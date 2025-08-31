"""
GitLab integration API routes.
"""
from fastapi import APIRouter, HTTPException, Depends

from core.logging_config import get_logger
from models.requests import RepositoryRequest
from models.responses import RepositoryResponse
from dependencies.service_dependencies import get_gitlab_service

logger = get_logger(__name__)
router = APIRouter(tags=["gitlab"])


@router.post("/get-repository", response_model=RepositoryResponse)
async def get_repository(request: RepositoryRequest, gitlab_service=Depends(get_gitlab_service)):
    """获取 GitLab 仓库信息"""
    logger.info(f"收到获取仓库请求: {request.repository_url}")
    
    result = gitlab_service.get_repository_info(request.repository_url)
    
    if result["status"] == "success":
        return RepositoryResponse(**result)
    else:
        raise HTTPException(status_code=500, detail=result["message"])