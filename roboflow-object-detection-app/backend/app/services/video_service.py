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
    # CREAR CARPETAS
    # =========================

    os.makedirs(
        "app/static/uploads",
        exist_ok=True
    )

    os.makedirs(
        "app/static/outputs",
        exist_ok=True
    )

    # =========================
    # ARCHIVO TEMPORAL
    # =========================

    temp_output = (
        f"app/static/outputs/temp_{filename}.avi"
    )

    # =========================
    # ABRIR VIDEO
    # =========================

    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():

        raise Exception(
            "Error opening video file"
        )

    # =========================
    # INFO VIDEO
    # =========================

    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    if fps <= 0:
        fps = 20

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

    print(f"[VIDEO] FPS: {fps}")
    print(f"[VIDEO] SIZE: {width}x{height}")

    # =========================
    # VIDEO WRITER
    # =========================

    fourcc = cv2.VideoWriter_fourcc(
        *'mp4v'
    )

    out = cv2.VideoWriter(
        temp_output,
        fourcc,
        fps,
        (width, height)
    )

    # =========================
    # VALIDAR WRITER
    # =========================

    if not out.isOpened():

        raise Exception(
            "Error creating video writer"
        )

    # =========================
    # PROCESAR FRAMES
    # =========================

    frame_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        # =========================
        # PROCESAR SOLO
        # 1 DE CADA 5 FRAMES
        # =========================

        if frame_count % 5 != 0:

            frame_count += 1

            continue

        print(f"[FRAME] {frame_count}")

        temp_frame = (
            f"app/static/uploads/frame_{frame_count}.jpg"
        )

        # =========================
        # GUARDAR FRAME
        # =========================

        cv2.imwrite(
            temp_frame,
            frame
        )

        # =========================
        # INFERENCIA
        # =========================

        result = await predict_image(
            temp_frame
        )

        predictions = result.get(
            "predictions",
            []
        )

        print(
            f"[PREDICTIONS] {len(predictions)}"
        )

        # =========================
        # DIBUJAR DETECCIONES
        # =========================

        frame = draw_detections(
            frame,
            predictions
        )

        # =========================
        # ESCRIBIR FRAME
        # =========================

        out.write(frame)

        # =========================
        # BORRAR TEMP
        # =========================

        if os.path.exists(temp_frame):

            os.remove(temp_frame)

        frame_count += 1

    # =========================
    # LIBERAR RECURSOS
    # =========================

    cap.release()

    out.release()

    cv2.destroyAllWindows()

    print("[INFO] Video processing finished")

    # =========================
    # CONVERTIR A MP4
    # =========================

    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-i",
        temp_output,
        "-vcodec",
        "libx264",
        "-acodec",
        "aac",
        output_path
    ]

    process = subprocess.run(
        ffmpeg_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    print(process.stdout.decode())
    print(process.stderr.decode())

    # =========================
    # VALIDAR OUTPUT
    # =========================

    if not os.path.exists(output_path):

        raise Exception(
            "FFmpeg failed to generate output video"
        )

    # =========================
    # BORRAR AVI TEMP
    # =========================

    if os.path.exists(temp_output):

        os.remove(temp_output)

    # =========================
    # RESPUESTA
    # =========================

    return {

        "success": True,

        "video_url": f"/static/outputs/{filename}.mp4"
    }