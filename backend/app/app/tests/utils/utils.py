import random
import string
from typing import Dict

from fastapi.testclient import TestClient

from core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


# def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
#     login_data = {
#         "email": settings.FIRST_SUPERUSER,
#         "password": settings.FIRST_SUPERUSER_PASSWORD,
#     }
#     r = client.post("/auth/jwt/login", data=login_data)
#     tokens = r.json()
#     a_token = tokens["access_token"]
#     headers = {"Authorization": f"Bearer {a_token}"}
#     return headers