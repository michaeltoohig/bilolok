from app.db.session import async_session
from app.db import base

from starlette import status
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.routing import Route
from starlette.templating import Jinja2Templates

from app.crud.user import CRUDUser
from app.crud.nakamal import CRUDNakamal
from app.crud.image import CRUDImage
from app.crud.checkin import CRUDCheckin
from app.crud.image import CRUDImage
from app.crud.image import CRUDImage
from app.crud.trip import CRUDTrip
from app.crud.video import CRUDVideo

templates = Jinja2Templates(directory="templates")


async def default(request):
    return templates.TemplateResponse("base.html", {"request": request})


async def user(request):
    id = request.path_params["id"]
    async with async_session() as db:
        crud_user = CRUDUser(db)
        user = await crud_user.get_by_id(id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return templates.TemplateResponse("user.html", {
        "request": request,
        "user": user,
    })


async def nakamal(request):
    id = request.path_params["id"]
    async with async_session() as db:
        crud_nakamal = CRUDNakamal(db)
        nakamal = await crud_nakamal.get_by_id(id)
        if not nakamal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        crud_image = CRUDImage(db)
        images = await crud_image.get_multi_by_nakamal(nakamal.id, limit=3)
    return templates.TemplateResponse("nakamal.html", {
        "request": request,
        "nakamal": nakamal,
        "title": f"{nakamal.name} on Bilolok!",
        "images": list(images),
    })


async def checkin(request):
    id = request.path_params["id"]
    async with async_session() as db:
        crud_checkin = CRUDCheckin(db)
        checkin = await crud_checkin.get_by_id(id)
        if not checkin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        crud_image = CRUDImage(db)
        images = await crud_image.get_multi_by_nakamal(checkin.nakamal.id, limit=1)
    return templates.TemplateResponse("checkin.html", {
        "request": request,
        "checkin": checkin,
        "title": f"Check-in at {checkin.nakamal.name} on Bilolok!",
        "images": list(images),
    })


async def image(request):
    id = request.path_params["id"]
    async with async_session() as db:
        crud_image = CRUDImage(db)
        image = await crud_image.get_by_id(id)
        if not image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return templates.TemplateResponse("image.html", {
        "request": request,
        "image": image,
        "title": f"Image of {image.nakamal.name} on Bilolok!",
    })


async def trip(request):
    id = request.path_params["id"]
    async with async_session() as db:
        crud_trip = CRUDTrip(db)
        trip = await crud_trip.get_by_id(id)
        if not trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return templates.TemplateResponse("trip.html", {
        "request": request,
        "trip": trip,
        "title": f"Trip to {trip.nakamal.name} on Bilolok!",
    })


async def video(request):
    id = request.path_params["id"]
    async with async_session() as db:
        crud_video = CRUDVideo(db)
        video = await crud_video.get_by_id(id)
        if not video:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return templates.TemplateResponse("video.html", {
        "request": request,
        "video": video,
    })
    

routes = [
    Route("/", default),
    Route("/user/{id:uuid}", user),
    Route("/nakamal/{id:uuid}", nakamal),
    Route("/checkin/{id:uuid}", checkin),
    Route("/image/{id:uuid}", image),
    Route("/trip/{id:uuid}", trip),
    Route("/video/{id:uuid}", video),
    Route("/{path:path}", default),
]


async def handle_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse("base.html", {"request": request})


exception_handlers = {
    404: handle_error,
    Exception: handle_error,
}


def startup():
    print("Ready to go")


app = Starlette(
    debug=True,
    routes=routes,
    exception_handlers=exception_handlers,
    on_startup=[startup],
)
