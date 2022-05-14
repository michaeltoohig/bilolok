import os
from pathlib import Path
from uuid import UUID
from PIL import Image, ImageOps

from loguru import logger

from app.core.config import settings
from app.crud.video import CRUDVideo
from app.models.video import VideoProcessingStatus
from app.schemas.video import VideoSchemaUpdate


def make_social_video(sfp: Path):
    ffp = sfp.parent / sfp.name.replace(sfp.suffix, ".mp4")
    os.system(f"{settings.FFMPEG_COMMAND} -i {str(sfp)} -movflags faststart -profile:v high -level 4.2 {str(ffp)}")
    logger.info(f"Complete transcode video to mp4 for social sharing")


def make_social_thumbnail(thumbnail: Path, watermark: Path, ffp: Path):
    BORDER = 120
    logger.info(f"Creating social thumbnail of {str(thumbnail)} and {str(watermark)}")
    img = Image.open(str(thumbnail))
    wm = Image.open(str(watermark))
    # Expand a white border around thumbnail to reach minimum 600px requirement of FB
    img = ImageOps.expand(img, border=BORDER, fill=(255,255,255))
    logger.debug("Expanded border of thumbnail")
    # resize watermark to fit border
    ratio = (BORDER / float(wm.size[1]))
    w = int((float(wm.size[0])*float(ratio)))
    wm = wm.resize((w,BORDER), Image.Resampling.LANCZOS)
    logger.debug("Resized watermark")
    # paste watermark around border of image
    center = img.size[0] // 2
    adj_center = center - (wm.size[0] // 2)
    # top watermark
    img.paste(wm, (adj_center,0), wm)
    # bottom watermark
    wm = wm.transpose(Image.Transpose.ROTATE_180)
    img.paste(wm, (adj_center,img.size[1]-BORDER), wm)
    # right side watermark
    wm = wm.transpose(Image.Transpose.ROTATE_90)
    center = img.size[1] // 2
    adj_center = center - (wm.size[1] // 2)
    img.paste(wm, (img.size[0]-BORDER,adj_center), wm)
    # left side watermark
    wm = wm.transpose(Image.Transpose.ROTATE_180)
    img.paste(wm, (0,adj_center), wm)
    logger.debug("Added watermark to thumbnail")
    img.save(str(ffp))


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
            watermark = Path(settings.DATA_LOCAL_DIR) / "images" / "watermark.png"
            assert watermark.exists()
            sfp = Path(settings.DATA_LOCAL_DIR) / crud_video._original_filepath(video)
            logger.debug(f"Got video {str(video.id)} original path {str(sfp)}")
            ffp = Path(settings.DATA_LOCAL_DIR) / crud_video._video_filepath(video)
            logger.debug(f"Got video {str(video.id)} final path {str(ffp)}")
            # webm video
            os.system(f"{settings.FFMPEG_COMMAND} -i {str(sfp)} -i {str(watermark)} -filter_complex '[1:v]scale=180:-2[z];[0:v][z]overlay[out]' -map '[out]' -map '0:a?' -c:v libvpx -qmin 0 -qmax 25 -crf 4 -b:v 500k -acodec libvorbis {str(ffp)}")
            logger.info(f"Complete transcode video {str(video.id)}")
            # cover image
            ffp = Path(settings.DATA_LOCAL_DIR) / crud_video._cover_filepath(video)
            os.system(f"{settings.FFMPEG_COMMAND} -i {str(sfp)} -vf 'select=eq(n\,0)' -q:v 3 {str(ffp)}")
            logger.info(f"Complete cover of video {str(video.id)}")
            video = await crud_video.update(
                video.id,
                VideoSchemaUpdate(status=VideoProcessingStatus.COMPLETE),
            )
            logger.info("Creating additional variations for social media")
            make_social_video(ffp)
            social_fp = Path(settings.DATA_LOCAL_DIR) / crud_video._social_thumbnail_filepath(video)
            make_social_thumbnail(ffp, watermark, social_fp)
        except Exception as exc:
            logger.error(f"Video {str(video.id)} failed")
            video = await crud_video.update(
                video.id,
                VideoSchemaUpdate(status=VideoProcessingStatus.ERROR),
            )
        await db.commit()
