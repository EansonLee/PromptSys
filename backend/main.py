from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import logging
from dotenv import load_dotenv
from datetime import datetime
import json

from services.prompt_generator import PromptGenerator

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

class PromptResponse(BaseModel):
    role: str
    goal: str
    function_output: str
    ui_requirements: str
    fixed_content: str
    theme_type: str
    raw_gpt_output: str
    timestamp: str

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

@app.post("/generate-prompt", response_model=PromptResponse)
async def generate_prompt(request: PromptRequest):
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