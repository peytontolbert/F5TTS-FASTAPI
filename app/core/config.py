from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "F5-TTS API"
    PORT: int = int(os.getenv("PORT", "8081"))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # TTS Settings
    MODEL_DIR: str = os.getenv("MODEL_DIR", "weights")
    VOICE_PROFILES_DIR: str = os.getenv("VOICE_PROFILES_DIR", "voice_profiles")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    class Config:
        case_sensitive = True

settings = Settings() 