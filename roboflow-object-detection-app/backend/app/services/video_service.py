import cv2
import os
import subprocess

from app.services.roboflow_service import predict_image
from app.utils.draw_utils import draw_detections


async def process_video(input_path, output_path, filename):

    # =========================
    # DIRECTORIOS
    # =========================

    os.makedirs("app/static/uploads", exist_ok=True)
    os.makedirs("app/static/outputs", exist_ok=True)

    temp_output = f"app/static/outputs/temp_{filename}.avi"

    # =========================
    # VIDEO INPUT
    # =========================

    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        raise Exception("Error opening video file")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 20

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"[VIDEO] FPS: {fps}")
    print(f"[VIDEO] SIZE: {width}x{height}")

    # =========================
    # WRITER (MP4 COMPATIBLE BASE)
    # =========================

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    out = cv2.VideoWriter(
        temp_output,
        fourcc,
        fps,
        (width, height)
    )

    if not out.isOpened():
        raise Exception("Error creating video writer")

    # =========================
    # PROCESS FRAMES
    # =========================

    frame_count = 0
    processed_frames = 0

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        # 🔥 FIX IMPORTANTE: skip correcto
        if frame_count % 5 != 0:
            frame_count += 1
            continue

        print(f"[FRAME] {frame_count}")

        temp_frame = f"app/static/uploads/frame_{frame_count}.jpg"

        cv2.imwrite(temp_frame, frame)

        # =========================
        # INFERENCE
        # =========================

        try:
            result = await predict_image(temp_frame)
            predictions = result.get("predictions", [])
        except Exception as e:
            print(f"[ERROR INFERENCE] {e}")
            predictions = []

        print(f"[PREDICTIONS] {len(predictions)}")

        # =========================
        # DRAW BOXES
        # =========================

        frame = draw_detections(frame, predictions)

        # =========================
        # WRITE FRAME
        # =========================

        out.write(frame)

        # =========================
        # CLEAN TEMP FRAME
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

    print(f"[INFO] Video finished. Frames processed: {processed_frames}")

    # =========================
    # FINAL CONVERSION (SAFE FFMEG)
    # =========================

    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-i",
        temp_output,
        "-vcodec",
        "libx264",
        "-preset",
        "ultrafast",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        output_path
    ]

    result = subprocess.run(
        ffmpeg_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    print(result.stderr.decode())

    # =========================
    # VALIDATION
    # =========================

    if not os.path.exists(output_path):
        raise Exception("FFmpeg failed to generate output video")

    # =========================
    # CLEAN TEMP
    # =========================

    if os.path.exists(temp_output):
        os.remove(temp_output)

    return {
        "success": True,
        "video_url": f"/static/outputs/{filename}.mp4"
    }