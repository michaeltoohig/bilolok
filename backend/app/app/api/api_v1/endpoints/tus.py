from enum import Enum
from pathlib import Path
from typing import Any, List, Optional
from app.core.arq_app import get_arq_app

from loguru import logger
import jwt
from fastapi import Body, Depends, Header, HTTPException, status, APIRouter
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi_users.jwt import JWT_ALGORITHM
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.api.deps.db import get_db
from app.api.deps.user import current_superuser
from app.core.config import settings
from app.core.users import UserManager, get_jwt_strategy, get_user_manager
from app.crud.image import CRUDImage
from app.crud.nakamal import CRUDNakamal
from app.crud.user import CRUDUser
from app.crud.video import CRUDVideo
from app.models.image import Image
from app.models.user import User
from app.schemas.image import ImageSchema, ImageSchemaIn, ImageSchemaOut
from app.schemas.video import VideoSchemaIn

router = APIRouter()


class UploadTarget(Enum):
    NAKAMAL = "NAKAMAL"
    NAKAMAL_VIDEO = "NAKAMAL_VIDEO"
    USER_PROFILE = "USER_PROFILE"
    USER_VIDEO = "USER_VIDEO"


@router.post(
    "/tus-hook",
    include_in_schema=False,
)
async def tus_hook(
    db: AsyncSession = Depends(get_db),
    user_manager: UserManager = Depends(get_user_manager),
    *,
    hook_name: str = Header(...),
    tusdIn: Any = Body(...),
) -> Any:
    """
    Hook for tusd.

    Now that I've added multiple targets for uploaded images this endpoint has become
    less than ideal. Could use some duplicate code reduced and maybe even functions
    to handle each individual target rather than if -> elif -> elif pattern.
    """
    crud_image = CRUDImage(db)
    crud_nakamal = CRUDNakamal(db)
    crud_user = CRUDUser(db)
    # Check JWT is valid
    scheme, _, token = (
        tusdIn.get("HTTPRequest").get("Header").get("Authorization")[0].partition(" ")
    )
    assert scheme == "Bearer"
    try:
        jwt_strategy = get_jwt_strategy()
        data = jwt.decode(
            token,
            jwt_strategy.secret,
            audience=jwt_strategy.token_audience,
            algorithms=[JWT_ALGORITHM],
        )
        user_id = data.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        # Check user is verified and active or superuser
        user = await user_manager.get(user_id)
        status_code = status.HTTP_401_UNAUTHORIZED
        if user:
            status_code = status.HTTP_403_FORBIDDEN
            if not user.is_active:
                status_code = status.HTTP_401_UNAUTHORIZED
                user = None
            if not user.is_verified:
                user = None
        if not user:
            raise HTTPException(status_code=status_code)
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Check upload target
    try:
        target = tusdIn.get("Upload").get("MetaData").get("Target")
        target = UploadTarget(target)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Target is not valid"
        )

    if target in [UploadTarget.NAKAMAL, UploadTarget.NAKAMAL_VIDEO]:
        # Check Nakamal exists
        nakamal_id = tusdIn.get("Upload").get("MetaData").get("NakamalID")
        nakamal = await crud_nakamal.get_by_id(nakamal_id)
        if not nakamal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal not found."
            )

    if hook_name == "post-finish":
        # Below could be some sort of task that handles image storage
        #  using the `.info` file in the uploads directory
        file_id = tusdIn.get("Upload").get("ID")
        filename = tusdIn.get("Upload").get("MetaData").get("filename")
        filetype = tusdIn.get("Upload").get("MetaData").get("filetype")
        if target == UploadTarget.NAKAMAL:
            try:
                # TODO a envvar should set the tusUpload directory for docker-compose file and in our settings the same
                #  For now this is a dirty hard-coded path
                tusUpload = Path(settings.DATA_LOCAL_DIR) / "uploads" / file_id
                assert tusUpload.exists()
                crud_image.save_file(
                    tusUpload, nakamal_id=nakamal_id, file_id=file_id, filename=filename
                )
                # Remove Tus `.info` file
                tusInfo = Path(str(tusUpload) + ".info")
                tusInfo.unlink()
            except Exception:
                # TODO log
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            try:
                in_schema = ImageSchemaIn(
                    file_id=file_id,
                    filename=filename,
                    filetype=filetype,
                    user_id=user_id,
                    nakamal_id=nakamal_id,
                )
                image = await crud_image.create(in_schema=in_schema)
                # Set image as profile if no images exist for nakamal
                priofile = await crud_image.get_current_nakamal_profile(nakamal_id)
                if not priofile:
                    await crud_image.create_nakamal_profile(image)
            except Exception as exc:
                # TODO log
                logger.exception("Error saving image to database or setting profile")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif target == UploadTarget.USER_PROFILE:
            try:
                # TODO a envvar should set the tusUpload directory for docker-compose file and in our settings the same
                #  For now this is a dirty hard-coded path
                tusUpload = Path(settings.DATA_LOCAL_DIR) / "uploads" / file_id
                assert tusUpload.exists()
                await crud_user.save_avatar(
                    tusUpload, user=user, file_id=file_id, filename=filename
                )
                # Remove Tus `.info` file
                tusInfo = Path(str(tusUpload) + ".info")
                tusInfo.unlink()
            except Exception:
                # TODO log
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif target == UploadTarget.USER_VIDEO:
            try:
                tusUpload = Path(settings.DATA_LOCAL_DIR) / "uploads" / file_id
                assert tusUpload.exists()
                crud_video = CRUDVideo(db)
                crud_video.save_file(tusUpload, user_id=user_id, file_id=file_id, filename=filename)
                logger.debug("Complete video save_file")
                # Remove Tus `.info` file
                tusInfo = Path(str(tusUpload) + ".info")
                tusInfo.unlink()
            except Exception:
                # TODO log
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            try:
                arq_app = await get_arq_app()
                in_schema = VideoSchemaIn(
                    file_id=file_id,
                    filename=filename,
                    filetype=filetype,
                    user_id=user_id,
                )
                video = await crud_video.create(in_schema=in_schema)
                logger.debug("Complete video save to db")
                await arq_app.enqueue_job(
                    "process_video", str(video.id),
                )
            except Exception:
                # TODO log
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif target == UploadTarget.NAKAMAL_VIDEO:
            try:
                tusUpload = Path(settings.DATA_LOCAL_DIR) / "uploads" / file_id
                assert tusUpload.exists()
                crud_video = CRUDVideo(db)
                crud_video.save_file(tusUpload, user_id=user_id, file_id=file_id, filename=filename)
                logger.debug("Complete video save_file")
                # Remove Tus `.info` file
                tusInfo = Path(str(tusUpload) + ".info")
                tusInfo.unlink()
            except Exception:
                # TODO log
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            try:
                arq_app = await get_arq_app()
                in_schema = VideoSchemaIn(
                    file_id=file_id,
                    filename=filename,
                    filetype=filetype,
                    user_id=user_id,
                    nakamal_id=nakamal_id,
                )
                video = await crud_video.create(in_schema=in_schema)
                logger.debug("Complete nakamal video save to db")
                await arq_app.enqueue_job(
                    "process_video", str(video.id),
                )
            except Exception:
                # TODO log
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)