from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.db import get_db
from app.crud.nakamal import CRUDNakamal
from app.db.errors import DoesNotExist
from app.schemas.nakamal import NakamalSchema


async def get_nakamal_or_404(
    db: AsyncSession = Depends(get_db),
    *,
    item_id: UUID,
) -> NakamalSchema:
    crud_nakamal = CRUDNakamal(db)
    try:
        item = await crud_nakamal.get_by_id(item_id)
        return item
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


# async def get_nakamal_resource_or_404(
#     db: AsyncSession = Depends(get_db),
#     *,
#     resource_id: UUID,
# ) -> NakamalResourceSchema:
#     crud_resource = CRUDNakamalResource(db)
#     resource = await crud_resource.get_by_id(resource_id)
#     if not resource:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal Resource not found."
#         )