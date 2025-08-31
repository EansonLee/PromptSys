"""
Health check API routes.
"""
from datetime import datetime
from fastapi import APIRouter

from core.logging_config import get_logger
from models.responses import HealthResponse

logger = get_logger(__name__)
router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Application health check endpoint."""
    logger.info("健康检查请求")
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat()
    )