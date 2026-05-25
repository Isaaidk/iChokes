import cv2

from app.services.roboflow_service import predict_image
from app.utils.draw_utils import draw_detections

async def process_image(
    input_path,
    output_path,
    filename
):

    result = await predict_image(input_path)

    image = cv2.imread(input_path)

    predictions = result.get(
        "predictions",
        []
    )

    image = draw_detections(
        image,
        predictions
    )

    cv2.imwrite(
        output_path,
        image
    )

    return {
        "predictions": predictions,
        "output_path": f"static/outputs/{filename}.jpg"
    }