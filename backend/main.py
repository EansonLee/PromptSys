"""
FastAPI application entry point with clean architecture.

This is the main entry point for the Prompt Generation API.
The application follows a clean architecture pattern with:
- Separation of concerns between API routes, business logic, and configuration
- Dependency injection for service management
- Centralized configuration and logging
- Modular route organization
- Backward compatibility for existing endpoints
"""
import uvicorn
from core.app_factory import create_application
from core.config import settings
from core.logging_config import get_logger

# Create application instance using factory pattern
app = create_application()

logger = get_logger(__name__)


if __name__ == "__main__":
    logger.info(f"启动服务器 - Host: {settings.backend_host}, Port: {settings.backend_port}")
    uvicorn.run(
        "main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=True  # Enable auto-reload during development
    )