"""
Middleware configuration for the FastAPI application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .logging_config import get_logger

logger = get_logger(__name__)


def setup_cors_middleware(app: FastAPI) -> None:
    """Configure CORS middleware for the FastAPI application."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    logger.info(f"CORS middleware configured with origins: {settings.cors_origins}")


def setup_middleware(app: FastAPI) -> None:
    """Setup all middleware for the FastAPI application."""
    setup_cors_middleware(app)