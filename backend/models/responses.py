"""
Pydantic response models for API endpoints.
"""
from pydantic import BaseModel
from typing import Dict, Any, Optional


class PromptResponse(BaseModel):
    """Response model for prompt generation."""
    role: str
    goal: str
    function_output: str
    ui_requirements: str
    fixed_content: str
    theme_type: str
    raw_gpt_output: str
    timestamp: str


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    timestamp: str


class SuccessResponse(BaseModel):
    """Generic success response model."""
    status: str
    message: str
    timestamp: str
    data: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Error response model."""
    status: str
    message: str
    error_code: Optional[str] = None
    timestamp: str


class ClaudeCliResponse(BaseModel):
    """Response model for Claude CLI operations."""
    status: str
    message: str
    timestamp: Optional[str] = None


class RepositoryResponse(BaseModel):
    """Response model for repository operations."""
    status: str
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class TaskResponse(BaseModel):
    """Response model for task operations."""
    status: str
    message: str
    prompt_file: Optional[str] = None
    timestamp: str