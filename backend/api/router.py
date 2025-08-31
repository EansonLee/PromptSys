"""
Central router configuration for all API endpoints.
"""
from fastapi import APIRouter
from .routes import prompt_routes, claude_routes, gitlab_routes, health_routes


def create_routers():
    """Create and configure all API routers."""
    
    # Create main API router with versioning
    api_router = APIRouter(prefix="/api/v1")
    api_router.include_router(prompt_routes.router)
    api_router.include_router(claude_routes.router) 
    api_router.include_router(gitlab_routes.router)
    api_router.include_router(health_routes.router)
    
    # Create legacy router for backward compatibility
    # This ensures existing frontend code continues to work
    legacy_router = APIRouter()
    legacy_router.include_router(prompt_routes.router)
    legacy_router.include_router(claude_routes.router)
    legacy_router.include_router(gitlab_routes.router)
    legacy_router.include_router(health_routes.router)
    
    return api_router, legacy_router