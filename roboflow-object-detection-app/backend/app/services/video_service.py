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
    # BASE DIR
    # =========================

    BASE_DIR = os.getcwd()

    UPLOAD_DIR = os.path.join(
        BASE_DIR,
        "backend/app/static/uploads"
    )

    OUTPUT_DIR = os.path.join(
        BASE_DIR,
        "backend/app/static/outputs"
    )

    # =========================
    # CREATE DIRECTORIES
    # =========================

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    # =========================
    # TEMP OUTPUT
    # =========================

    temp_output = os.path.join(
        OUTPUT_DIR,
        f"temp_{filename}.mp4"
    )

    # =========================
    # FINAL OUTPUT
    # =========================

    final_output = os.path.join(
        OUTPUT_DIR,
        f"{filename}.mp4"
    )

    # =========================
    # OPEN VIDEO
    # =========================

    cap = cv2.VideoCapture(
        input_path
    )

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
    # FRAME SKIP
    # =========================

    FRAME_SKIP = 5

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

        temp_frame = os.path.join(
            UPLOAD_DIR,
            f"frame_{frame_count}.jpg"
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
        f"[INFO] Video finished. Frames processed: {processed_frames}"
    )

    # =========================
    # VALIDATE TEMP VIDEO
    # =========================

    if not os.path.exists(temp_output):

        raise Exception(
            "Temporary video was not created"
        )

    # =========================
    # FFMPEG CONVERSION
    # =========================

    ffmpeg_command = [
        "ffmpeg",
        "-y",

        "-i",
        temp_output,

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

        final_output
    ]

    process = subprocess.run(
        ffmpeg_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    print(process.stdout.decode())
    print(process.stderr.decode())

    # =========================
    # VALIDATE FINAL VIDEO
    # =========================

    if not os.path.exists(final_output):

        raise Exception(
            "FFmpeg failed to generate output video"
        )

    print(f"[OUTPUT] Saved: {final_output}")

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