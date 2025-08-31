"""
Centralized configuration management for the FastAPI application.
"""
import os
import logging
from typing import List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv

# Force load .env file, overriding system environment variables
load_dotenv(override=True)

logger = logging.getLogger(__name__)


class Settings(BaseModel):
    """Application settings with environment variable integration."""
    
    # API Configuration
    app_title: str = "Prompt Generation API"
    app_version: str = "1.0.0"
    
    # Server Configuration
    backend_host: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    openai_base_url: Optional[str] = os.getenv("OPENAI_BASE_URL")
    siliconflow_api_key: Optional[str] = os.getenv("SILICONFLOW_API_KEY")
    
    # CORS Configuration
    cors_origins: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    # Logging Configuration
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    def validate_required_settings(self) -> None:
        """Validate that all required settings are present."""
        logger.info("=== 系统配置检查 ===")
        
        if self.openai_api_key:
            logger.info(f"✓ OPENAI_API_KEY: {self.openai_api_key[:20]}...")
        else:
            logger.warning("✗ OPENAI_API_KEY 未配置")
        
        if self.openai_base_url:
            logger.info(f"✓ OPENAI_BASE_URL: {self.openai_base_url}")
        else:
            logger.warning("✗ OPENAI_BASE_URL 未配置，将使用默认 OpenAI API")
        
        logger.info(f"✓ CORS Origins: {self.cors_origins}")
        logger.info("=== 配置检查完成 ===")

    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings()