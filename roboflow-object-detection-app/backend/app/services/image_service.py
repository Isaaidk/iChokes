import cv2
import os

from app.services.roboflow_service import predict_image
from app.utils.draw_utils import draw_detections


async def process_image(input_path, output_path, filename):

    try:

        # =========================
        # DIRECTORIOS SEGURIDAD
        # =========================

        os.makedirs("app/static/uploads", exist_ok=True)
        os.makedirs("app/static/outputs", exist_ok=True)

        # =========================
        # VALIDAR INPUT
        # =========================

        if not os.path.exists(input_path):
            raise Exception(f"Input image not found: {input_path}")

        # =========================
        # LEER IMAGEN
        # =========================

        image = cv2.imread(input_path)

        if image is None:
            raise Exception("cv2 failed to read image (invalid file or format)")

        print(f"[IMAGE] Loaded: {input_path}")

        # =========================
        # INFERENCIA (ROBUSTA)
        # =========================

        try:
            result = await predict_image(input_path)
            predictions = result.get("predictions", [])
        except Exception as e:
            print(f"[ROBoflow ERROR] {e}")
            predictions = []

        print(f"[PREDICTIONS] {len(predictions)}")

        # =========================
        # DRAW DETECTIONS
        # =========================

        image = draw_detections(image, predictions)

        # =========================
        # SAVE OUTPUT
        # =========================

        success = cv2.imwrite(output_path, image)

        if not success:
            raise Exception("Failed to save output image (cv2.imwrite failed)")

        print(f"[OUTPUT] Saved: {output_path}")

        # =========================
        # FINAL VALIDATION
        # =========================

        if not os.path.exists(output_path):
            raise Exception("Output file not created")

        # =========================
        # RESPONSE
        # =========================

        return {
            "success": True,
            "predictions": predictions,
            "output_path": f"/static/outputs/{filename}.jpg"
        }

    except Exception as e:
        print(f"[PROCESS IMAGE ERROR] {str(e)}")
        raise Exception(str(e))