from fastapi import APIRouter, UploadFile, File
from app.services.video_service import process_video
import shutil
import uuid

from app.services.image_service import process_image

router = APIRouter()

UPLOAD_DIR = "app/static/uploads/"
OUTPUT_DIR = "app/static/outputs/"

@router.post("/predict-image")
async def predict_image_route(
    file: UploadFile = File(...)
):

    file_id = str(uuid.uuid4())

    input_path = f"{UPLOAD_DIR}{file_id}.jpg"

    output_path = f"{OUTPUT_DIR}{file_id}.jpg"

    with open(input_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    result = await process_image(
        input_path,
        output_path,
        file_id
    )

    return result

@router.post("/predict-video")
async def predict_video_route(
    file: UploadFile = File(...)
):

    file_id = str(uuid.uuid4())

    input_path = (
        f"{UPLOAD_DIR}{file_id}.mp4"
    )

    output_path = (
        f"{OUTPUT_DIR}{file_id}.mp4"
    )

    with open(input_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    result = await process_video(
        input_path,
        output_path,
        file_id
    )

    return result