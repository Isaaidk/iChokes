import cv2
import os

from app.services.roboflow_service import predict_image
from app.utils.draw_utils import draw_detections


async def process_image(
    input_path,
    output_path,
    filename
):

    try:

        # =========================
        # VALIDAR INPUT
        # =========================

        if not os.path.exists(input_path):

            raise Exception(
                "Input image not found"
            )

        # =========================
        # LEER IMAGEN
        # =========================

        image = cv2.imread(input_path)

        if image is None:

            raise Exception(
                "Failed to read image"
            )

        print(f"[IMAGE] Loaded: {input_path}")

        # =========================
        # INFERENCIA ROBOFLOW
        # =========================

        result = await predict_image(
            input_path
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

        image = draw_detections(
            image,
            predictions
        )

        # =========================
        # CREAR CARPETA OUTPUT
        # =========================

        os.makedirs(
            "app/static/outputs",
            exist_ok=True
        )

        # =========================
        # GUARDAR RESULTADO
        # =========================

        success = cv2.imwrite(
            output_path,
            image
        )

        if not success:

            raise Exception(
                "Failed to save output image"
            )

        print(
            f"[OUTPUT] Saved: {output_path}"
        )

        # =========================
        # RESPUESTA
        # =========================

        return {
            "success": True,
            "predictions": predictions,
            "output_path": f"/static/outputs/{filename}.jpg"
        }

    except Exception as e:

        print(f"[PROCESS IMAGE ERROR] {str(e)}")

        raise Exception(str(e))