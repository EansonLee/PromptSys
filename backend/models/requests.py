"""
Pydantic request models for API endpoints.
"""
from pydantic import BaseModel
from typing import Dict, Any


class PromptRequest(BaseModel):
    """Request model for prompt generation."""
    app_name: str
    theme: str
    variant_folder: str
    ui_color: str = "蓝色科技感"
    reference_file: str = ""
    tab_count: int = 3


class RepositoryRequest(BaseModel):
    """Request model for repository operations."""
    repository_url: str


class TaskRequest(BaseModel):
    """Request model for task operations."""
    selected_prompt: Dict[str, Any]