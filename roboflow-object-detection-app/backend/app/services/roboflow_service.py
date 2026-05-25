from inference_sdk import InferenceHTTPClient

from app.core.config import settings

client = InferenceHTTPClient(
    api_url=settings.API_URL,
    api_key=settings.ROBOFLOW_API_KEY
)

async def predict_image(image_path: str):

    result = client.infer(
        image_path,
        model_id=settings.MODEL_ID
    )

    return result