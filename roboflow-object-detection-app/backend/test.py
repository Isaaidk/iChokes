from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="pfwbgZ7odti0u4iqrM1D"
)

result = CLIENT.infer(
    "test.jpg",
    model_id="accident-detection-njsyf/4"
)

print(result)
