import cv2
from pathlib import Path

from app.services.roboflow_service import predict_image
from app.utils.draw_utils import draw_detections


async def process_image(
    input_path,
    output_path,
    filename
):

    # =========================
    # PATHS ABSOLUTOS
    # =========================

    BASE_DIR = Path(__file__).resolve().parent.parent

    outputs_dir = BASE_DIR / "static" / "outputs"

    outputs_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    absolute_output = outputs_dir / f"{filename}.jpg"

    # =========================
    # LEER IMAGEN
    # =========================

    image = cv2.imread(str(input_path))

    if image is None:

        raise Exception(
            "Failed to read image"
        )

    # =========================
    # INFERENCIA
    # =========================

    result = await predict_image(
        input_path
    )

    predictions = result.get(
        "predictions",
        []
    )

    # =========================
    # DIBUJAR
    # =========================

    image = draw_detections(
        image,
        predictions
    )

    # =========================
    # GUARDAR
    # =========================

    success = cv2.imwrite(
        str(absolute_output),
        image
    )

    if not success:

        raise Exception(
            "Failed saving image"
        )

    print(f"[OUTPUT SAVED] {absolute_output}")

    # =========================
    # RESPONSE
    # =========================

    return {

        "success": True,

        "predictions": predictions,

        "output_path":
            f"/static/outputs/{filename}.jpg"
    }