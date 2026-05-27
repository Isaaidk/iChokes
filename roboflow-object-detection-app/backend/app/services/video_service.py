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

    # =========================
    # DIRECTORIES
    # =========================

    os.makedirs(
        "backend/app/static/uploads",
        exist_ok=True
    )

    os.makedirs(
        "backend/app/static/outputs",
        exist_ok=True
    )

    # =========================
    # TEMP FILE
    # =========================

    temp_output = (
        f"backend/app/static/outputs/temp_{filename}.mp4"
    )

    # =========================
    # OPEN VIDEO
    # =========================

    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():

        raise Exception(
            "Error opening video file"
        )

    # =========================
    # VIDEO INFO
    # =========================

    original_fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    if original_fps <= 0:
        original_fps = 20

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

    print(f"[VIDEO] FPS: {original_fps}")
    print(f"[VIDEO] SIZE: {width}x{height}")

    # =========================
    # SKIP FRAMES
    # =========================

    FRAME_SKIP = 5

    # 🔥 FIX:
    # FPS REAL DEL VIDEO FINAL
    output_fps = max(
        original_fps / FRAME_SKIP,
        1
    )

    print(f"[OUTPUT FPS] {output_fps}")

    # =========================
    # VIDEO WRITER
    # =========================

    fourcc = cv2.VideoWriter_fourcc(
        *"mp4v"
    )

    out = cv2.VideoWriter(
        temp_output,
        fourcc,
        output_fps,
        (width, height)
    )

    if not out.isOpened():

        raise Exception(
            "Error creating video writer"
        )

    # =========================
    # PROCESS FRAMES
    # =========================

    frame_count = 0
    processed_frames = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        # =========================
        # SKIP FRAMES
        # =========================

        if frame_count % FRAME_SKIP != 0:

            frame_count += 1
            continue

        print(f"[FRAME] {frame_count}")

        temp_frame = (
            f"backend/app/static/uploads/frame_{frame_count}.jpg"
        )

        # =========================
        # SAVE TEMP FRAME
        # =========================

        cv2.imwrite(
            temp_frame,
            frame
        )

        # =========================
        # INFERENCE
        # =========================

        try:

            result = await predict_image(
                temp_frame
            )

            predictions = result.get(
                "predictions",
                []
            )

        except Exception as e:

            print(f"[ERROR INFERENCE] {e}")

            predictions = []

        print(
            f"[PREDICTIONS] {len(predictions)}"
        )

        # =========================
        # DRAW DETECTIONS
        # =========================

        frame = draw_detections(
            frame,
            predictions
        )

        # =========================
        # WRITE FRAME
        # =========================

        out.write(frame)

        # =========================
        # DELETE TEMP FRAME
        # =========================

        if os.path.exists(temp_frame):

            os.remove(temp_frame)

        frame_count += 1
        processed_frames += 1

    # =========================
    # RELEASE
    # =========================

    cap.release()
    out.release()

    cv2.destroyAllWindows()

    print(
        f"[INFO] Frames processed: {processed_frames}"
    )

    # =========================
    # FINAL FFMEG CONVERSION
    # =========================

    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-i",
        temp_output,

        # 🔥 MOBILE SAFE
        "-c:v",
        "libx264",

        "-preset",
        "fast",

        "-pix_fmt",
        "yuv420p",

        "-movflags",
        "+faststart",

        "-profile:v",
        "baseline",

        "-level",
        "3.0",

        output_path
    ]

    process = subprocess.run(
        ffmpeg_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    print(process.stderr.decode())

    # =========================
    # VALIDATE OUTPUT
    # =========================

    if not os.path.exists(output_path):

        raise Exception(
            "FFmpeg failed to generate output video"
        )

    # =========================
    # DELETE TEMP VIDEO
    # =========================

    if os.path.exists(temp_output):

        os.remove(temp_output)

    # =========================
    # RESPONSE
    # =========================

    return {

        "success": True,

        "video_url": f"/static/outputs/{filename}.mp4"
    }