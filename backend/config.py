"""
Configuration management for the Mistral Fact Checker API
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Configuration
    mistral_api_key: str
    api_title: str = "Mistral Fact Checker API"
    api_description: str = "API for fact-checking content using Mistral AI"
    api_version: str = "1.0.0"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS Configuration
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # Mistral AI Configuration
    mistral_text_model: str = "mistral-large-latest"
    mistral_vision_model: str = "pixtral-large-latest"
    mistral_temperature: float = 0.3
    
    # Request Limits
    max_text_length: int = 10000
    max_url_content_length: int = 10000
    max_image_size_mb: int = 10
    url_timeout_seconds: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

