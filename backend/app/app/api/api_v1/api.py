from fastapi import APIRouter

from api.api_v1.endpoints import (auth, checkins, chiefs, images, nakamalAreas,
                                      nakamalKavaSources, nakamalResources,
                                      nakamals, subscriptions, trips, tus, users,
                                      utils, videos)

api_router = APIRouter()

api_router.include_router(auth.auth_router, prefix="/auth/jwt", tags=["auth"])
api_router.include_router(auth.register_router, prefix="/auth", tags=["auth"])
api_router.include_router(auth.reset_password_router, prefix="/auth", tags=["auth"])
api_router.include_router(auth.verify_router, prefix="/auth", tags=["auth"])

api_router.include_router(users.router, prefix="/users", tags=["users"])

api_router.include_router(checkins.router, tags=["checkins"])
api_router.include_router(images.router, tags=["images"])
api_router.include_router(nakamals.router, tags=["nakamals"])
api_router.include_router(nakamalAreas.router, tags=["nakamals"])
api_router.include_router(nakamalKavaSources.router, tags=["nakamals"])
api_router.include_router(nakamalResources.router, tags=["nakamals"])
api_router.include_router(chiefs.router, tags=["chiefs", "checkins"])
api_router.include_router(subscriptions.router, tags=["subscriptions"])
api_router.include_router(trips.router, tags=["trips"])
api_router.include_router(utils.router, tags=["utils"])
api_router.include_router(videos.router, tags=["videos"])

api_router.include_router(tus.router)
