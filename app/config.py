import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Resolve base directory path
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    environment: str = "development"
    
    # OpenAI Settings
    openai_api_key: str = ""
    
    # Redis Settings
    redis_url: str = "redis://localhost:6379/0"
    
    # Database Settings
    database_url: str = "sqlite:///./petcare.db"
    
    # Vector DB Settings
    vector_store: str = "faiss"
    pinecone_api_key: str | None = None
    pinecone_env: str | None = None
    
    # Paths
    data_dir: str = str(BASE_DIR / "data")
    faq_dir: str = str(BASE_DIR / "data" / "faq")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
