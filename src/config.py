from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, RedisDsn, validator
from typing import List, Dict

class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ALLOWED_ORIGINS: List[AnyHttpUrl]
    REDIS_URL: RedisDsn
    BACKEND_SERVICES: Dict[str, str]

    class Config:
        env_file = ".env"

    @validator("ALLOWED_ORIGINS", pre=True)
    def assemble_allowed_origins(cls, v: str) -> List[str]:
        return [i.strip() for i in v.split(",")]

    @validator("BACKEND_SERVICES", pre=True)
    def assemble_backend_services(cls, v: str) -> Dict[str, str]:
        services = v.split(",")
        return {service.strip(): service.strip() for service in services}

settings = Settings()