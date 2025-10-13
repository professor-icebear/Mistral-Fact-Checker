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
    # Can be set via environment variable as comma-separated string
    # e.g., CORS_ORIGINS="http://localhost:3000,https://your-app.netlify.app"
    cors_origins: str = "http://localhost:3000,http://localhost:3001"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins to list"""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
    
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

