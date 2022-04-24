import os
from pathlib import Path
from uuid import UUID

from loguru import logger

from app.core.config import settings
from app.crud.video import CRUDVideo
from app.models.video import VideoProcessingStatus
from app.schemas.video import VideoSchemaUpdate


async def process_video(ctx: dict, item_id: UUID):
    db_session = ctx["db_session"]
    async with db_session() as db:
        crud_video = CRUDVideo(db)
        video = await crud_video.get_by_id(item_id)
        if not video:
            return "Video not found."
        try:
            video = await crud_video.update(
                video.id,
                VideoSchemaUpdate(status=VideoProcessingStatus.PROGRESS),
            )
            logger.info(f"Got video {str(video.id)}")
            # transcoded file
            sfp = Path(settings.DATA_LOCAL_DIR) / crud_video._original_filepath(video)
            logger.debug(f"Got video {str(video.id)} original path {str(sfp)}")
            # sfp = crud_video.build_full_filepath(ofp)
            ffp = Path(settings.DATA_LOCAL_DIR) / crud_video._video_filepath(video)
            logger.debug(f"Got video {str(video.id)} final path {str(ffp)}")
            os.system(f"ffmpeg -i {str(sfp)} -c:v libvpx -qmin 0 -qmax 25 -crf 4 -b:v 500k -vf scale=540:-2 -an {str(ffp)}")
            logger.info(f"Complete transcode video {str(video.id)}")
            # cover image
            ffp = Path(settings.DATA_LOCAL_DIR) / crud_video._cover_filepath(video)
            os.system(f"ffmpeg -i {str(sfp)} -vf 'select=eq(n\,0)' -q:v 3 {str(ffp)}")
            logger.info(f"Complete cover of video {str(video.id)}")
            video = await crud_video.update(
                video.id,
                VideoSchemaUpdate(status=VideoProcessingStatus.COMPLETE),
            )
        except Exception as exc:
            logger.error(f"Video {str(video.id)} failed")
            video = await crud_video.update(
                video.id,
                VideoSchemaUpdate(status=VideoProcessingStatus.ERROR),
            )
        await db.commit()
