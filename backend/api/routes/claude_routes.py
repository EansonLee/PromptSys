"""
Claude CLI automation API routes.
"""
import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends

from core.logging_config import get_logger
from models.requests import TaskRequest
from models.responses import ClaudeCliResponse, TaskResponse, SuccessResponse
from dependencies.service_dependencies import get_claude_cli_service

logger = get_logger(__name__)
router = APIRouter(tags=["claude"])


@router.post("/open-claude-cli", response_model=ClaudeCliResponse)
async def open_claude_cli(claude_service=Depends(get_claude_cli_service)):
    """打开 Claude CLI - 跨平台实现"""
    logger.info("收到打开 Claude CLI 请求")
    
    result = claude_service.open_claude_cli()
    
    if result["status"] == "success":
        return ClaudeCliResponse(**result)
    else:
        raise HTTPException(status_code=500, detail=result["message"])


@router.post("/get-tasks", response_model=TaskResponse)
async def get_tasks(request: TaskRequest, claude_service=Depends(get_claude_cli_service)):
    """将选中的提示词传递给 Claude CLI"""
    logger.info("收到获取任务请求")
    
    try:
        file_path = claude_service.write_prompt_to_file(request.selected_prompt)
        
        return TaskResponse(
            status="success",
            message="任务已成功传递给 Claude CLI",
            prompt_file=file_path,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"获取任务失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取任务失败: {str(e)}")


@router.post("/execute-tasks", response_model=ClaudeCliResponse)
async def execute_tasks(claude_service=Depends(get_claude_cli_service)):
    """执行 Claude CLI 任务"""
    logger.info("收到执行任务请求")
    
    try:
        # 查找最新的提示词文件
        temp_dir = os.path.join(os.getcwd(), "temp_claude")
        if not os.path.exists(temp_dir):
            raise HTTPException(status_code=400, detail="未找到任务文件，请先获取任务")
        
        # 获取最新的提示词文件
        prompt_files = [f for f in os.listdir(temp_dir) if f.startswith("claude_prompt_") and f.endswith(".txt")]
        if not prompt_files:
            raise HTTPException(status_code=400, detail="未找到任务文件，请先获取任务")
        
        # 选择最新的文件
        latest_file = max(prompt_files, key=lambda x: os.path.getmtime(os.path.join(temp_dir, x)))
        prompt_file_path = os.path.join(temp_dir, latest_file)
        
        result = claude_service.execute_claude_command(prompt_file_path)
        
        if result["status"] == "success":
            return ClaudeCliResponse(**result)
        else:
            raise HTTPException(status_code=500, detail=result["message"])
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"执行任务失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"执行任务失败: {str(e)}")


@router.post("/cleanup-temp-files", response_model=SuccessResponse)
async def cleanup_temp_files(claude_service=Depends(get_claude_cli_service)):
    """清理临时文件"""
    logger.info("收到清理临时文件请求")
    
    result = claude_service.cleanup_temp_files()
    return SuccessResponse(**result, timestamp=datetime.now().isoformat())