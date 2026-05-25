from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.video_service import process_video
from app.services.image_service import process_image

import shutil
import uuid
import os

router = APIRouter()

UPLOAD_DIR = "app/static/uploads/"
OUTPUT_DIR = "app/static/outputs/"

# Crear carpetas automáticamente
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.post("/predict-image")
async def predict_image_route(
    file: UploadFile = File(...)
):

    try:

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

    except Exception as e:

        print(f"[ERROR IMAGE] {str(e)}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/predict-video")
async def predict_video_route(
    file: UploadFile = File(...)
):

    try:

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

    except Exception as e:

        print(f"[ERROR VIDEO] {str(e)}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )