from pathlib import Path
from typing import List, Type

from sqlalchemy import select

from core.config import settings
from crud.base import CRUDBase
from models.user import User
from schemas.user import UserCreate, UserSchema, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserSchema]):
    @property
    def _in_schema(self) -> Type[UserCreate]:
        return UserCreate

    @property
    def _schema(self) -> Type[UserSchema]:
        return UserSchema

    @property
    def _table(self) -> Type[User]:
        return User

    async def save_avatar(
        self, sfp: Path, *, user: UserSchema, file_id: str, filename: str,
    ):
        """Save the given file to it's storage path defined by `filepath`."""
        new_filename = "{f_id}{ext}".format(f_id=file_id, ext=Path(filename).suffix)
        ffp = Path(settings.DATA_LOCAL_DIR) / self._table.build_avatar_filepath(
            user.id, new_filename
        )
        ffp.parent.mkdir(parents=True, exist_ok=True)
        sfp.replace(
            str(ffp)
        )  # removes original and assumes both are on same filesystem
        # update user model with new avatar filename
        update_schema = UserUpdate(**user.dict())
        update_schema.avatar_filename = new_filename
        await self.update(user.id, update_schema=update_schema)

    async def get_multi(self) -> List[UserSchema]:
        query = select(self._table).where(self._table.is_active == True)
        results = (await self._db_session.execute(query)).scalars()
        return (self._schema.from_orm(item) for item in results)
