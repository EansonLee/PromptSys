"""
Centralized logging configuration for the FastAPI application.
"""
import logging
from .config import settings


def configure_logging() -> None:
    """Configure application-wide logging settings."""
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Configure specific loggers if needed
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level: {settings.log_level}")


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance."""
    return logging.getLogger(name)