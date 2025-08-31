"""
Prompt generation API routes.
"""
import json
import asyncio
from datetime import datetime
from typing import AsyncGenerator
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse

from core.logging_config import get_logger
from models.requests import PromptRequest
from models.responses import PromptResponse
from services.prompt_generator import PromptGenerator
from dependencies.service_dependencies import get_prompt_generator

logger = get_logger(__name__)
router = APIRouter(tags=["prompts"])


async def generate_prompt_stream(
    request: PromptRequest,
    prompt_generator: PromptGenerator
) -> AsyncGenerator[str, None]:
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


@router.post("/generate-prompt", response_model=PromptResponse)
async def generate_prompt(
    request: PromptRequest,
    prompt_generator: PromptGenerator = Depends(get_prompt_generator)
):
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


@router.post("/generate-prompt-stream")
async def generate_prompt_stream_endpoint(
    request: PromptRequest,
    prompt_generator: PromptGenerator = Depends(get_prompt_generator)
):
    """新的流式API接口，提供实时进度更新"""
    logger.info(f"收到流式提示词生成请求 - APP: {request.app_name}, 主题: {request.theme[:50]}...")
    
    return StreamingResponse(
        generate_prompt_stream(request, prompt_generator),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # 防止nginx缓冲
        }
    )