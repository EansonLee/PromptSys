"""
FastAPI application factory with clean configuration.
"""
from fastapi import FastAPI
from core.config import settings
from core.logging_config import configure_logging, get_logger
from core.middleware import setup_middleware
from api.router import create_routers

logger = get_logger(__name__)


def create_application() -> FastAPI:
    """
    Application factory function that creates and configures the FastAPI app.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    # Configure logging first
    configure_logging()
    
    # Validate configuration
    settings.validate_required_settings()
    
    # Create FastAPI application
    app = FastAPI(
        title=settings.app_title,
        version=settings.app_version,
        description="A scalable prompt generation API with Claude CLI automation and GitLab integration"
    )
    
    # Setup middleware
    setup_middleware(app)
    
    # Create and include routers
    api_router, legacy_router = create_routers()
    app.include_router(api_router)
    app.include_router(legacy_router)
    
    logger.info(f"Application '{settings.app_title}' v{settings.app_version} created successfully")
    logger.info(f"API documentation available at: http://{settings.backend_host}:{settings.backend_port}/docs")
    
    return app