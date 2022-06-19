from unittest import mock

import uuid
from app.tests.utils.nakamal import create_random_area, create_random_kava_source
from app.tests.utils.user import create_random_user, user_authentication_headers
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.crud.nakamal import CRUDNakamal
from app.schemas.nakamal import NakamalSchemaIn

pytestmark = pytest.mark.asyncio


async def test_nakamal_create(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    area = await create_random_area(db_session=db_session)
    kava_source = await create_random_kava_source(db_session=db_session)
    crud_nakamals = CRUDNakamal(db_session)
    payload = {
        "name": "Whatever",
        "lat": 0,
        "lng": 0,
        "light": "White",
        "owner": None,
        "phone": None,
        "windows": 1,
        "area_id": str(area.id),
        "kava_source_id": str(kava_source.id),
    }

    email, password = await create_random_user()
    headers = await user_authentication_headers(client=client, email=email, password=password)
    response = await client.post("/nakamals", json=payload, headers=headers)

    # XXX SQLAlchemy Base class `default` id value of `uuid.uuid4` is not being set in tests but works in normal context
    assert response.status_code == status.HTTP_201_CREATED

    nakamal = await crud_nakamals.get_by_id(response.json()["id"])
    data = response.json()
    data["name"] == payload["name"]
    data["id"] == str(nakamal.id)