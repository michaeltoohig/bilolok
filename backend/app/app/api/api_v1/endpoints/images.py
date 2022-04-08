from enum import Enum
from pathlib import Path
from typing import Any, List, Optional
from app.api.deps.db import get_db
from app.crud.nakamal import CRUDNakamal
from app.schemas.user import UserSchema, UserUpdate

import jwt
from fastapi import Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi import status, Body, HTTPException, Header
from fastapi_users.jwt import JWT_ALGORITHM

from app.crud.image import CRUDImage
from app.crud.user import CRUDUser
from app.api.deps.user import current_superuser
from app.core.config import settings
from app.core.users import UserManager, get_user_manager, get_jwt_strategy
from app.models.image import Image
from app.models.user import User
from app.schemas.image import ImageSchemaIn, ImageSchema, ImageSchemaOut
from sqlalchemy.ext.asyncio.session import AsyncSession


# TODO remove this CRUDRouter as we are no longer even using it due to special schema handling
router = SQLAlchemyCRUDRouter(
    prefix="images",
    tags=["images"],
    schema=ImageSchema,
    create_schema=ImageSchemaIn,
    db_model=Image,
    db=get_db,
    get_one_route=False,
    get_all_route=False,
    delete_all_route=False,
    update_route=False,
    create_route=False,
    delete_one_route=False,
)


@router.get("", response_model=List[ImageSchemaOut])
async def get_all(
    db: AsyncSession = Depends(get_db),
    *,
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
) -> Any:
    crud_image = CRUDImage(db)
    images = await crud_image.get_multi(skip=skip, limit=limit)
    return [ImageSchemaOut(**image.dict()) for image in images]


@router.get("/{item_id}", response_model=ImageSchemaOut)
async def get_one(
    db: AsyncSession = Depends(get_db),
    *,
    item_id: str
) -> Any:
    crud_image = CRUDImage(db)
    image = await crud_image.get_by_id(item_id)
    return ImageSchemaOut(**image.dict())


@router.delete("/{item_id}", response_model=ImageSchemaOut)
async def delete_one(
    db: AsyncSession = Depends(get_db),
    superuser: User = Depends(current_superuser),
    *,
    item_id: str
) -> Any:
    crud_image = CRUDImage(db)
    image = await crud_image.delete(item_id)
    return ImageSchemaOut(**image.dict())


class UploadTarget(Enum):
    NAKAMAL = "NAKAMAL"
    USER_PROFILE = "USER_PROFILE"


@router.post("/tus-hook", include_in_schema=False,)
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
    scheme, _, token = tusdIn.get("HTTPRequest").get("Header").get("Authorization")[0].partition(" ")
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
            if not user.is_verified or not user.is_superuser:
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Target is not valid")
    
    if target == UploadTarget.NAKAMAL:    
        # Check Nakamal exists
        nakamal_id = tusdIn.get("Upload").get("MetaData").get("NakamalID")
        nakamal = await crud_nakamal.get_by_id(nakamal_id)
        if not nakamal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal not found.")

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
                tusUpload = Path(settings.IMAGES_LOCAL_DIR) / "uploads" / file_id
                assert tusUpload.exists()
                crud_image.save_file(tusUpload, nakamal_id=nakamal_id, file_id=file_id, filename=filename)
                # Remove Tus `.info` file
                tusInfo = Path(str(tusUpload) + ".info")
                tusInfo.unlink()
            except Exception as exc:
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
            except Exception as exc:
                # TODO log
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif target == UploadTarget.USER_PROFILE:
            try:
                # TODO a envvar should set the tusUpload directory for docker-compose file and in our settings the same
                #  For now this is a dirty hard-coded path
                tusUpload = Path(settings.IMAGES_LOCAL_DIR) / "uploads" / file_id
                assert tusUpload.exists()
                await crud_user.save_avatar(tusUpload, user=user, file_id=file_id, filename=filename)
                # Remove Tus `.info` file
                tusInfo = Path(str(tusUpload) + ".info")
                tusInfo.unlink()
            except Exception as exc:
                # TODO log
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
