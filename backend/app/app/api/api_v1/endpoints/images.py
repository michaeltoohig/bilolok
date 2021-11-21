from pathlib import Path
from typing import Any, List, Optional

import jwt
from fastapi import Depends
from fastapi_crudrouter import OrmarCRUDRouter
from fastapi import status, Body, HTTPException, Header
from fastapi_users.jwt import JWT_ALGORITHM

from app import crud
from app.api.deps import current_superuser
from app.core.config import settings
from app.core.users import jwt_authentication
from app.models.image import Image
# from app.schemas.image import ImageCreate, ImageDB


router = OrmarCRUDRouter(
    schema=Image,
    prefix="images",
    tags=["images"],
    get_one_route=False,
    get_all_route=False,
    delete_all_route=False,
    update_route=False,
    create_route=False,
    delete_one_route=[Depends(current_superuser)],
)


@router.get("", response_model=List[Image])
async def get_all(
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
) -> Any:
    images = await crud.image.get_multi(skip=skip, limit=limit)
    return images


@router.get("/{item_id}", response_model=Image)
async def get_one(
    item_id: str
) -> Any:
    image = await crud.image.get(item_id)
    return image


@router.post("/tus-hook", include_in_schema=False,)
async def tus_hook(
    hook_name: str = Header(...),
    tusdIn: Any = Body(...),
) -> Any:
    """
    Hook for tusd.
    """
    # Check JWT is valid    
    _, token = tusdIn.get("HTTPRequest").get("Header").get("Authorization")[0].split(" ")
    try:
        data = jwt.decode(
            token,
            jwt_authentication.secret,
            audience=jwt_authentication.token_audience,
            algorithms=[JWT_ALGORITHM],
        )
        user_id = data.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Check Nakamal exists
    nakamal_id = tusdIn.get("Upload").get("MetaData").get("NakamalID")
    nakamal = await crud.nakamal.get(nakamal_id)
    if not nakamal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal not found.")

    if hook_name == "post-finish":
        # Below could be some sort of task that handles image storage 
        #  using the `.info` file in the uploads directory
        file_id = tusdIn.get("Upload").get("ID")
        filename = tusdIn.get("Upload").get("MetaData").get("filename")
        filetype = tusdIn.get("Upload").get("MetaData").get("filetype")
        try:
            # TODO a envvar should set the tusUpload directory for docker-compose file and in our settings the same
            #  For now this is a dirty hard-coded path
            tusUpload = Path(settings.IMAGES_LOCAL_DIR) / "uploads" / file_id
            assert tusUpload.exists()
            crud.image.save_file(tusUpload, nakamal_id=nakamal_id, file_id=file_id, filename=filename)
            # Remove Tus `.info` file
            tusInfo = Path(str(tusUpload) + ".info")
            tusInfo.unlink()
        except Exception as exc:
            print(exc)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            obj_in = ImageCreate(
                file_id=file_id,
                filename=filename,
                filetype=filetype,
                user_id=user_id,
                nakamal_id=nakamal_id,
            )
            image = await crud.image.create(obj_in=obj_in)
        except Exception as exc:
            print(exc)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
