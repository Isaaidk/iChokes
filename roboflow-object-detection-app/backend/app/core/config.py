from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    ROBOFLOW_API_KEY: str

    MODEL_ID: str

    API_URL: str

    class Config:
        env_file = ".env"

settings = Settings()