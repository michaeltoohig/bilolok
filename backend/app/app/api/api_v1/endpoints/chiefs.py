from typing import List, Optional
from pydantic import UUID4

from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.api.deps.db import get_db
from app.crud.nakamal import CRUDNakamal
from app.crud.user import CRUDUser
from app.schemas.nakamal import NakamalSchemaOut

router = APIRouter(prefix="/chiefs")


@router.get(
    "",
    response_model=List[NakamalSchemaOut],
)
async def get_all(
    db: AsyncSession = Depends(get_db),
    # *,
    # skip: Optional[int] = 0,
    # limit: Optional[int] = 100,
) -> List[NakamalSchemaOut]:
    crud_nakamal = CRUDNakamal(db)
    nakamals = await crud_nakamal.get_chiefs()
    return [NakamalSchemaOut(**nakamal.dict()) for nakamal in nakamals]


@router.get(
    "/{item_id:uuid}",
    response_model=List[NakamalSchemaOut],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "detail": "User not found.",
        },
    },
)
async def get_one(
    db: AsyncSession = Depends(get_db),
    *,
    item_id: UUID4
) -> List[NakamalSchemaOut]:
    """A user's current chief titles"""
    # TODO user dependency
    crud_user = CRUDUser(db)
    item = await crud_user.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    crud_nakamal = CRUDNakamal(db)
    nakamals = await crud_nakamal.get_multi_by_chief(item_id)
    return [NakamalSchemaOut(**nakamal.dict()) for nakamal in nakamals]