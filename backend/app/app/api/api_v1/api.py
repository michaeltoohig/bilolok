from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    auth,
    checkins,
    images,
    nakamals,
    users,
    utils,
)

api_router = APIRouter()


api_router.include_router(auth.auth_router, prefix="/auth/jwt", tags=["auth"])
api_router.include_router(auth.register_router, prefix="/auth", tags=["auth"])
api_router.include_router(auth.reset_password_router, prefix="/auth", tags=["auth"])
api_router.include_router(auth.verify_router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, tags=["utils"])

api_router.include_router(checkins.router, tags=["checkins"])
api_router.include_router(images.router, tags=["images"])
api_router.include_router(nakamals.router, tags=["nakamals"])
