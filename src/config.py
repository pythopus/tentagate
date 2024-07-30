from pydantic import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ALLOWED_ORIGINS: list = ["*"]
    REDIS_URL: str
    BACKEND_SERVICES: dict

    class Config:
        env_file = ".env"

settings = Settings()