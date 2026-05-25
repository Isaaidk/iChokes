import cv2
import os
import subprocess

from app.services.roboflow_service import predict_image
from app.utils.draw_utils import draw_detections

async def process_video(
    input_path,
    output_path,
    filename
):

    temp_output = (
        f"app/static/outputs/temp_{filename}.avi"
    )

    cap = cv2.VideoCapture(input_path)

    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    width = int(
        cap.get(
            cv2.CAP_PROP_FRAME_WIDTH
        )
    )

    height = int(
        cap.get(
            cv2.CAP_PROP_FRAME_HEIGHT
        )
    )

    fourcc = cv2.VideoWriter_fourcc(
        *'XVID'
    )

    out = cv2.VideoWriter(
        temp_output,
        fourcc,
        fps,
        (width, height)
    )

    frame_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        temp_frame = (
            f"app/static/uploads/frame_{frame_count}.jpg"
        )

        cv2.imwrite(
            temp_frame,
            frame
        )

        result = await predict_image(
            temp_frame
        )

        predictions = result.get(
            "predictions",
            []
        )

        frame = draw_detections(
            frame,
            predictions
        )

        out.write(frame)

        os.remove(temp_frame)

        frame_count += 1

    cap.release()

    out.release()

    # Convertir AVI -> MP4 H264 compatible navegador
    subprocess.run([
        "ffmpeg",
        "-y",
        "-i",
        temp_output,
        "-vcodec",
        "libx264",
        "-acodec",
        "aac",
        output_path
    ])

    os.remove(temp_output)

    return {
        "video_url": f"static/outputs/{filename}.mp4"
    }