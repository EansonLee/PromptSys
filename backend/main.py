from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import os
import logging
from dotenv import load_dotenv
from datetime import datetime
import json
import asyncio
from typing import AsyncGenerator
import platform
import subprocess
import requests

from services.prompt_generator import PromptGenerator
from services.claude_cli_automation import claude_cli_automation
from services.gitlab_integration import gitlab_integration

# 强制加载.env文件，覆盖系统环境变量
load_dotenv(override=True)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Prompt Generation API")

# 从环境变量获取CORS配置
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
logger.info(f"✓ CORS Origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    app_name: str
    theme: str
    variant_folder: str
    ui_color: str = "蓝色科技感"
    reference_file: str = ""
    tab_count: int = 3

class PromptResponse(BaseModel):
    role: str
    goal: str
    function_output: str
    ui_requirements: str
    fixed_content: str
    theme_type: str
    raw_gpt_output: str
    timestamp: str

class RepositoryRequest(BaseModel):
    repository_url: str

class TaskRequest(BaseModel):
    selected_prompt: dict

# 启动时检查配置
logger.info("=== 系统配置检查 ===")
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_base_url = os.getenv("OPENAI_BASE_URL")

if openai_api_key:
    logger.info(f"✓ OPENAI_API_KEY: {openai_api_key[:20]}...")
else:
    logger.warning("✗ OPENAI_API_KEY 未配置")

if openai_base_url:
    logger.info(f"✓ OPENAI_BASE_URL: {openai_base_url}")
else:
    logger.warning("✗ OPENAI_BASE_URL 未配置，将使用默认 OpenAI API")

logger.info("=== 配置检查完成 ===")

prompt_generator = PromptGenerator()

async def generate_prompt_stream(request: PromptRequest) -> AsyncGenerator[str, None]:
    """生成提示词的流式生成器，提供进度更新"""
    try:
        # 步骤1: 初始化 (10%)
        yield f"data: {json.dumps({'progress': 10, 'status': '正在初始化...', 'step': '参数验证'})}\n\n"
        await asyncio.sleep(0.1)
        
        # 步骤2: 开始调用GPT (20%)
        yield f"data: {json.dumps({'progress': 20, 'status': '正在连接GPT模型...', 'step': 'GPT连接'})}\n\n"
        await asyncio.sleep(0.1)
        
        # 步骤3: GPT处理中 (30-80%)
        yield f"data: {json.dumps({'progress': 30, 'status': '正在生成创意内容...', 'step': 'GPT处理'})}\n\n"
        
        # 模拟GPT生成过程的进度更新
        for progress in range(35, 80, 5):
            await asyncio.sleep(0.2)
            status_messages = [
                '正在分析主题特征...',
                '正在设计创意功能...',
                '正在生成用户界面描述...',
                '正在优化内容结构...',
                '正在完善功能细节...',
                '正在整理输出格式...',
                '即将完成生成...'
            ]
            message_index = min(len(status_messages) - 1, (progress - 35) // 5)
            yield f"data: {json.dumps({'progress': progress, 'status': status_messages[message_index], 'step': 'GPT处理'})}\n\n"
        
        # 实际调用GPT生成内容
        logger.info("开始调用 GPT 模型生成内容...")
        gpt_output = await prompt_generator.generate(
            theme=request.theme,
            app_name=request.app_name,
            variant_folder=request.variant_folder,
            ui_color=request.ui_color,
            reference_file=request.reference_file
        )
        logger.info(f"GPT 生成完成，输出长度: {len(gpt_output)} 字符")
        
        # 步骤4: 解析格式化 (85%)
        yield f"data: {json.dumps({'progress': 85, 'status': '正在解析生成内容...', 'step': '内容解析'})}\n\n"
        await asyncio.sleep(0.1)
        
        # 解析并封装为模板格式
        logger.info("开始解析并封装模板格式...")
        template_result = prompt_generator.format_template(
            gpt_output=gpt_output,
            app_name=request.app_name,
            variant_folder=request.variant_folder,
            ui_color=request.ui_color,
            theme=request.theme,
            reference_file=request.reference_file
        )
        logger.info("模板格式化完成")
        
        # 步骤5: 完成 (100%)
        yield f"data: {json.dumps({'progress': 95, 'status': '正在封装最终结果...', 'step': '结果封装'})}\n\n"
        await asyncio.sleep(0.1)
        
        response = PromptResponse(
            role=template_result["role"],
            goal=template_result["goal"],
            function_output=template_result["function_output"],
            ui_requirements=template_result["ui_requirements"],
            fixed_content=template_result["fixed_content"],
            theme_type=template_result["theme_type"],
            raw_gpt_output=gpt_output,
            timestamp=datetime.now().isoformat()
        )
        
        # 发送完成状态和最终结果
        yield f"data: {json.dumps({'progress': 100, 'status': '生成完成！', 'step': '完成', 'result': response.dict()})}\n\n"
        
        logger.info(f"提示词生成成功 - APP: {request.app_name}")
        
    except Exception as e:
        logger.error(f"提示词生成失败: {str(e)}")
        yield f"data: {json.dumps({'error': str(e), 'progress': 0, 'status': '生成失败'})}\n\n"

@app.post("/generate-prompt", response_model=PromptResponse)
async def generate_prompt(request: PromptRequest):
    """保持原有的同步API接口，用于向后兼容"""
    logger.info(f"收到提示词生成请求 - APP: {request.app_name}, 主题: {request.theme[:50]}...")
    
    try:
        # 调用 GPT 生成内容
        logger.info("开始调用 GPT 模型生成内容...")
        gpt_output = await prompt_generator.generate(
            theme=request.theme,
            app_name=request.app_name,
            variant_folder=request.variant_folder,
            ui_color=request.ui_color,
            reference_file=request.reference_file
        )
        logger.info(f"GPT 生成完成，输出长度: {len(gpt_output)} 字符")
        
        # 解析并封装为模板格式
        logger.info("开始解析并封装模板格式...")
        template_result = prompt_generator.format_template(
            gpt_output=gpt_output,
            app_name=request.app_name,
            variant_folder=request.variant_folder,
            ui_color=request.ui_color,
            theme=request.theme,
            reference_file=request.reference_file
        )
        logger.info("模板格式化完成")
        
        response = PromptResponse(
            role=template_result["role"],
            goal=template_result["goal"],
            function_output=template_result["function_output"],
            ui_requirements=template_result["ui_requirements"],
            fixed_content=template_result["fixed_content"],
            theme_type=template_result["theme_type"],
            raw_gpt_output=gpt_output,
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"提示词生成成功 - APP: {request.app_name}")
        return response
        
    except Exception as e:
        logger.error(f"提示词生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-prompt-stream")
async def generate_prompt_stream_endpoint(request: PromptRequest):
    """新的流式API接口，提供实时进度更新"""
    logger.info(f"收到流式提示词生成请求 - APP: {request.app_name}, 主题: {request.theme[:50]}...")
    
    return StreamingResponse(
        generate_prompt_stream(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # 防止nginx缓冲
        }
    )

@app.post("/open-claude-cli")
async def open_claude_cli():
    """打开 Claude CLI - 跨平台实现"""
    logger.info("收到打开 Claude CLI 请求")
    
    result = claude_cli_automation.open_claude_cli()
    
    if result["status"] == "success":
        return result
    else:
        raise HTTPException(status_code=500, detail=result["message"])

@app.post("/get-repository")
async def get_repository(request: RepositoryRequest):
    """获取 GitLab 仓库信息"""
    logger.info(f"收到获取仓库请求: {request.repository_url}")
    
    result = gitlab_integration.get_repository_info(request.repository_url)
    
    if result["status"] == "success":
        return result
    else:
        raise HTTPException(status_code=500, detail=result["message"])

@app.post("/get-tasks")
async def get_tasks(request: TaskRequest):
    """将选中的提示词传递给 Claude CLI"""
    logger.info("收到获取任务请求")
    
    try:
        file_path = claude_cli_automation.write_prompt_to_file(request.selected_prompt)
        
        return {
            "status": "success",
            "message": "任务已成功传递给 Claude CLI",
            "prompt_file": file_path,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"获取任务失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取任务失败: {str(e)}")

@app.post("/execute-tasks")
async def execute_tasks():
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
        
        result = claude_cli_automation.execute_claude_command(prompt_file_path)
        
        if result["status"] == "success":
            return result
        else:
            raise HTTPException(status_code=500, detail=result["message"])
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"执行任务失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"执行任务失败: {str(e)}")

@app.post("/cleanup-temp-files")
async def cleanup_temp_files():
    """清理临时文件"""
    logger.info("收到清理临时文件请求")
    
    result = claude_cli_automation.cleanup_temp_files()
    return result

@app.get("/health")
async def health_check():
    logger.info("健康检查请求")
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    # 从环境变量获取服务器配置
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", "8000"))
    logger.info(f"启动服务器 - Host: {host}, Port: {port}")
    uvicorn.run(app, host=host, port=port)