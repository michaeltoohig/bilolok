from typing import Any, Dict, Optional, Union

# from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.nakamal import Nakamal, NakamalTable
from app.schemas.nakamal import NakamalCreate, NakamalUpdate


class CRUDNakamal(CRUDBase[Nakamal, NakamalCreate, NakamalUpdate]):
    pass


nakamal = CRUDNakamal(NakamalTable)
