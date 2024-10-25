# src/common/config/settings.py
from pydantic_settings import BaseSettings
from pydantic import validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Image Scaling Service"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    REDIS_URL: str = "redis://redis:6379"
    POSTGRES_DSN: str = "postgresql://user:password@postgres:5432/scaling_db"
    
    @validator('REDIS_URL', 'POSTGRES_DSN', pre=True)
    def check_urls(cls, v: str) -> str:
        if not v:
            raise ValueError("URL cannot be empty")
        return v
    
    class Config:
        env_file = ".env"

settings = Settings()