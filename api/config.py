"""
API configuration and settings.
"""
import os
from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """API configuration settings."""
    
    # API Settings
    API_TITLE: str = "CodeOracle API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "REST API for CodeOracle - AI-powered code analysis and orchestration"
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True  # Auto-reload in development
    
    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:5173",  # Vite default port
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Agent Settings
    AGENT_TIMEOUT: int = 300  # 5 minutes
    MAX_CONCURRENT_REQUESTS: int = 10
    CACHE_TTL: int = 3600  # 1 hour
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS: List[str] = [".json"]
    
    # IBM watsonx.ai Settings (from environment)
    WATSONX_API_KEY: str = os.getenv("WATSONX_API_KEY", "")
    WATSONX_PROJECT_ID: str = os.getenv("WATSONX_PROJECT_ID", "")
    WATSONX_URL: str = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
    
    # Model Settings
    MODEL_ID: str = "meta-llama/llama-3-1-70b-instruct"
    MAX_NEW_TOKENS: int = 4000
    TEMPERATURE: float = 0.1
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields from .env


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Application settings
    """
    return Settings()


# Logging configuration
def setup_logging():
    """Configure logging for the API."""
    import logging
    
    settings = get_settings()
    
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format=settings.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("codeoracle_api.log")
        ]
    )
    
    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    
    return logging.getLogger(__name__)


# Validate configuration
def validate_config():
    """
    Validate that required configuration is present.
    
    Raises:
        ValueError: If required configuration is missing
    """
    settings = get_settings()
    
    if not settings.WATSONX_API_KEY:
        raise ValueError("WATSONX_API_KEY environment variable is required")
    
    if not settings.WATSONX_PROJECT_ID:
        raise ValueError("WATSONX_PROJECT_ID environment variable is required")
    
    return True

# Made with Bob
