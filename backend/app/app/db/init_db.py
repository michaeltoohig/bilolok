from pathlib import Path
from tasks.video import make_social_thumbnail, make_social_video

from sqlalchemy.orm import Session

# from app import crud
from core.config import settings
from core.users import create_user
from db.session import async_engine, async_session
from schemas.user import UserCreate
from crud.video import CRUDVideo

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQLAlchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


async def init_db(db: Session) -> None:
    await create_user(settings.FIRST_SUPERUSER, settings.FIRST_SUPERUSER_PASSWORD, is_superuser=True)
    
    # async with async_engine.begin() as connection:
    #     async with async_session(bind=connection) as session:
    #         try:
    #             user_db = get_user_db(session)
    #             await fastapi_users.create_user(
    #                 UserCreate(
    #                     email=settings.FIRST_SUPERUSER,
    #                     password=settings.FIRST_SUPERUSER_PASSWORD,
    #                     is_active=True,
    #                     is_verified=True,
    #                     is_superuser=True,
    #                 )
    #             )
    #         except Exception:
    #             raise
    #             pass  # user already exists

            # # TODO remove in future release - only needed for one production release
            # watermark = Path(settings.DATA_LOCAL_DIR) / "images" / "watermark.png"
            # assert watermark.exists()
            # try:
            #     crud_video = CRUDVideo(session)
            #     videos = await crud_video.get_multi()
            #     for video in videos:
            #         src = Path(settings.DATA_LOCAL_DIR) / crud_video._video_filepath(video)
            #         social_src_path = src.parent / src.name.replace(src.suffix, ".mp4")
            #         if not social_src_path.exists(): 
            #             make_social_video(src)
            #         thumbnail = Path(settings.DATA_LOCAL_DIR) / crud_video._cover_filepath(video)
            #         social_thumbnail_path = Path(settings.DATA_LOCAL_DIR) / crud_video._social_thumbnail_filepath(video)
            #         if not social_thumbnail_path.exists():
            #             make_social_thumbnail(thumbnail, watermark, social_thumbnail_path)
            # except Exception as exc:
            #     print("Social thumbnail generation failed")
            #     raise