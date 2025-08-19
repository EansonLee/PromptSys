from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
import os
import json
import re
import logging

class PromptGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 配置详细日志
        logging.getLogger("httpx").setLevel(logging.DEBUG)
        logging.getLogger("openai").setLevel(logging.DEBUG)
        logging.getLogger("langchain").setLevel(logging.DEBUG)
        
        # 主要API配置
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        primary_model = os.getenv("OPENAI_MODEL", "gpt-4")
        temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        
        # 硅基流动降级配置
        fallback_api_key = os.getenv("SILICONFLOW_API_KEY", "sk-dummy-key")
        fallback_base_url = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
        fallback_model = os.getenv("SILICONFLOW_MODEL", "Qwen/Qwen2.5-32B-Instruct")
        
        # 保存配置为实例变量，用于日志记录
        self.fallback_base_url = fallback_base_url
        self.fallback_model = fallback_model
        
        self.logger.info(f"初始化LLM配置:")
        self.logger.info(f"  - Primary API Key: {api_key[:20] if api_key else 'None'}...")
        self.logger.info(f"  - Primary Base URL: {base_url}")
        self.logger.info(f"  - Primary Model: {primary_model}")
        self.logger.info(f"  - Temperature: {temperature}")
        self.logger.info(f"  - Fallback API Key: {fallback_api_key[:20] if fallback_api_key else 'None'}...")
        self.logger.info(f"  - Fallback Base URL: {fallback_base_url}")
        self.logger.info(f"  - Fallback Model: {fallback_model}")
        
        # 主要LLM配置
        self.primary_llm = ChatOpenAI(
            model=primary_model,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature
        )
        
        # 降级LLM配置（硅基流动）
        self.fallback_llm = ChatOpenAI(
            model=fallback_model,
            api_key=fallback_api_key,
            base_url=fallback_base_url,
            temperature=temperature
        )
        
        self.logger.info("提示词生成器初始化完成")
        
    async def generate(self, theme: str, app_name: str, variant_folder: str, ui_color: str = "蓝色科技感") -> str:
        """调用 GPT 生成提示词内容"""
        self.logger.info(f"开始生成提示词 - 主题: {theme[:30]}..., APP: {app_name}")
        
        system_prompt = """你是一位极具创意的 Android 开发工程师和提示词专家，擅长设计创新性、趣味性的移动应用功能。
根据用户输入的主题，生成一个充满创意和想象力的、带有两个创新小功能的 Fragment Prompt。

重要：输出必须是干净的JSON格式，不包含任何控制字符或特殊字符。

角色格式要求：
- 必须包含"Android 工具类 App 的创意开发工程师"
- 格式："你是一位 Android 工具类 App 的创意开发工程师，目标是在[APP名称]中新增一个名为[Fragment名称]的 Fragment，[创意描述]。"

目标格式要求：
- 必须以"参考 @TrafficJourneyFragment.kt 在 @{variant_folder}/ 变体下，"开头
- 然后跟随创意的目标描述

创意要求：
1. 功能设计必须严格围绕用户输入的主题进行，确保高度契合主题内容
2. 每个功能模块都要有独特的创意亮点和交互方式
3. 融入游戏化、社交化或个性化等创意元素
4. 使用生动有趣的比喻和场景描述
5. 输出必须严格遵循指定的JSON格式
6. 功能模块必须基于真实数据但以创意方式呈现
7. 包含详细的创意实现逻辑和UI要求
8. 功能输出要包含具体的示例展示
9. 仔细分析用户主题，确保功能模块与主题完全匹配
10. 不得省略或新增无关内容

**详细输出要求（重要）：**
- description字段必须包含3-5个详细的功能点，每个用"• "开头
- 每个功能点必须具体描述实现逻辑、数据来源、交互方式
- example字段必须包含具体数值、时间、百分比等真实数据示例
- 适当使用emoji表情符号增加趣味性
- UI要求必须包含具体的颜色代码、尺寸、动画效果描述
- 描述要生动形象，使用比喻和场景化语言

输出格式（严格按此格式）：
{
  "role": "你是一位 Android 工具类 App 的创意开发工程师，目标是在[APP名称]中新增一个名为[Fragment名称]的 Fragment，[创意描述]。",
  "goal": "参考 @TrafficJourneyFragment.kt 在 @{variant_folder}/ 变体下，构建一个以[主题]为主题的创意型 Fragment 页面，包含 2 个基于真实数据的小功能模块，并将数据本地存储以支持长期回顾。",
  "function_module_1": {
    "title": "### 功能模块1：[模块名称]（真实数据生成）",
    "description": "• [功能点1：具体实现逻辑，包含数据来源和处理方式]\\n• [功能点2：交互方式和用户体验设计]\\n• [功能点3：数据存储和展示逻辑]\\n• [功能点4：创意亮点和特色功能]\\n• [功能点5：游戏化或社交化元素（可选）]",
    "example": "示例展示：\\n📊 [具体数据示例，包含数值、时间、百分比等]\\n🎯 [展示格式说明，包含具体的界面布局描述]\\n⚡ [交互效果描述，包含动画和反馈效果]"
  },
  "function_module_2": {
    "title": "### 功能模块2：[模块名称]", 
    "description": "• [功能点1：具体实现逻辑，包含数据来源和处理方式]\\n• [功能点2：交互方式和用户体验设计]\\n• [功能点3：数据存储和展示逻辑]\\n• [功能点4：创意亮点和特色功能]\\n• [功能点5：与模块1的联动或差异化设计]",
    "example": "示例展示：\\n📈 [具体数据示例，包含数值、时间、百分比等]\\n🎨 [展示格式说明，包含具体的界面布局描述]\\n✨ [交互效果描述，包含动画和反馈效果]"
  },
  "ui_requirements": "- 主色调{ui_color}，主要颜色值#[具体色值]\\n- 卡片圆角半径8dp，阴影elevation 4dp\\n- 按钮高度48dp，文字大小16sp\\n- 列表项间距12dp，内边距16dp\\n- 加载动画时长300ms，使用缓入缓出效果\\n- 数据刷新使用下拉刷新，支持触觉反馈\\n- 图表使用渐变色填充，支持点击交互\\n- 空状态页面包含插画和引导文案"
}"""

        user_prompt = f"""主题：{theme}
APP名称：{app_name}
变体文件夹：{variant_folder}
UI主色调：{ui_color}

请生成一个干净的JSON格式的Fragment提示词。重要要求：
1. 输出必须是纯正的JSON，不包含任何控制字符或特殊符号
2. 严格按照角色和目标格式要求
3. 功能设计必须严格围绕主题"{theme}"进行，确保两个功能模块都与这个主题高度相关
4. 仔细分析主题关键词，确保功能创意完全符合主题需求
5. 融入趣味性、游戏化或社交化元素
6. 使用生动的比喻和场景化描述
7. 每个功能都要有创新的交互方式和视觉效果

**详细格式要求（重要）：**
- description必须包含3-5个功能点，每个用"• "开头，用\\n分隔
- 每个功能点必须详细描述实现逻辑、数据来源、交互方式
- example必须包含具体的数值、时间、百分比等真实数据
- 适当使用emoji表情符号（📊📈🎯🎨⚡✨等）增加趣味性
- UI要求必须包含具体的颜色代码、尺寸（dp/sp）、动画时长（ms）
- 描述要生动形象，使用比喻和场景化语言
- 示例展示格式：示例展示：\\n📊 [数据]\\n🎯 [布局]\\n⚡ [交互]

请直接返回JSON，不要添加任何其他文字。"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        self.logger.info("=== 准备发送请求到GPT ===")
        self.logger.info(f"System prompt长度: {len(system_prompt)}")
        self.logger.info(f"User prompt长度: {len(user_prompt)}")
        
        try:
            self.logger.info("开始调用主要LLM (GPT-4)...")
            response = await self.primary_llm.ainvoke(messages)
            self.logger.info(f"=== 主要LLM (GPT-4) 调用成功 ===")
            self.logger.info(f"使用API: {getattr(self.primary_llm, 'openai_api_base', 'default')}")
            self.logger.info(f"使用模型: {getattr(self.primary_llm, 'model_name', 'gpt-4')}")
            self.logger.info(f"返回内容长度: {len(response.content)}")
            self.logger.info(f"返回内容预览: {response.content[:200]}...")
            return response.content
        except Exception as e:
            self.logger.warning(f"=== 主要LLM调用失败，尝试降级策略 ===")
            self.logger.warning(f"主要LLM错误类型: {type(e).__name__}")
            self.logger.warning(f"主要LLM错误信息: {str(e)}")
            
            # 检查是否需要降级（429配额限制、500服务器错误、其他网络错误）
            error_str = str(e).lower()
            should_fallback = (
                "429" in str(e) or 
                "quota" in error_str or 
                "rate" in error_str or
                "500" in str(e) or
                "internal server error" in error_str or
                "internalservererror" in type(e).__name__.lower() or
                "server error" in error_str
            )
            
            if should_fallback:
                self.logger.info(f"检测到需要降级的错误: {type(e).__name__}，使用硅基流动降级策略")
                try:
                    self.logger.info("开始调用降级LLM (硅基流动 Qwen)...")
                    fallback_response = await self.fallback_llm.ainvoke(messages)
                    self.logger.info(f"=== 降级LLM (硅基流动 Qwen) 调用成功 ===")
                    self.logger.info(f"使用API: {self.fallback_base_url}")
                    self.logger.info(f"使用模型: {self.fallback_model}")
                    self.logger.info(f"降级LLM返回内容长度: {len(fallback_response.content)}")
                    self.logger.info(f"降级LLM返回内容预览: {fallback_response.content[:200]}...")
                    return fallback_response.content
                except Exception as fallback_error:
                    self.logger.error(f"=== 降级LLM调用也失败 ===")
                    self.logger.error(f"降级LLM错误类型: {type(fallback_error).__name__}")
                    self.logger.error(f"降级LLM错误信息: {str(fallback_error)}")
                    # 如果降级也失败，抛出原始错误
                    raise e
            else:
                # 如果不是可降级的错误，直接抛出原始错误
                self.logger.error(f"=== 非可降级错误，不使用降级策略 ===")
                self.logger.error(f"错误类型: {type(e).__name__}")
                self.logger.error(f"错误详情: {str(e)}")
                raise e
    
    def format_template(self, gpt_output: str, app_name: str, variant_folder: str, ui_color: str = "蓝色科技感") -> dict:
        """将GPT输出格式化为模板结构"""
        self.logger.info("开始解析GPT输出并格式化为模板")
        try:
            # 清理JSON字符串，移除控制字符
            self.logger.info("清理GPT输出中的控制字符")
            cleaned_output = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', gpt_output)
            
            # 解析JSON输出
            self.logger.info("尝试解析JSON格式的GPT输出")
            gpt_data = json.loads(cleaned_output)
            self.logger.info("JSON解析成功")
            
            # 构建功能输出
            function_output = f"""{gpt_data['function_module_1']['title']}

{gpt_data['function_module_1']['description']}

{gpt_data['function_module_1']['example']}

{gpt_data['function_module_2']['title']}

{gpt_data['function_module_2']['description']}

{gpt_data['function_module_2']['example']}"""

            # 添加固定内容
            fixed_content = """

### 5. 数据采集逻辑：
- 使用 @/module-wifi 中的工具类，参考 中获取WiFi列表的方式来获取周围网络列表
如需要跳转Dialog参考 
- 参考 @/module-wifi  中的工具类获取WiFi、信号等信息;
- 图表使用MpChart，参考 @FreeRankFragment.kt@free_fragment_rank.xml 中图表、流量获取的用法;
- 参考 @/module_fake 中使用数据库的方法进行数据库存储，在本变体中进行编写数据库文件即可

6. 权限说明：
参考 @/variant 中其他变体以及 @PermissionComplianceManager.kt 中的申请权限的方法修改;
当前变体，同一个权限使用同一个key

- 参考 @FreeRankFragment.kt 中申请应用使用权限的方法;
7. 参考 @SpeedFragment.kt 中Fragment的可见性逻辑，对 进行修改，不需要马上进行扫描，只有进入Fragment点击按钮，给了权限后才进行扫描;
8. 新建的 Fragment逻辑也跟第 7.一样;
9. 参考 @BabyAppAdapter.kt 新建"RecycleView"的"Adapter";
10. 参考 @BabyChangeDialog.kt 新建Dialog;
11. 参考 @BabyFlowChangeActivity.kt 新建Activity;
12. 参考 @StatisticsFragment.kt 中流量的获取、使用方法;
13. 都要真实数据，WiFi无信号，没WiFi、WiFi不可用，没信号直接展示无数据即可，不要生成、展示模拟数据"""

            # 格式化UI要求，确保每个要求都在单独的行
            ui_requirements = gpt_data["ui_requirements"].replace("{ui_color}", ui_color)
            # 如果UI要求没有换行符，尝试按句号或短横线分割并添加换行
            if "\\n" not in ui_requirements and "\n" not in ui_requirements:
                # 按句号或短横线分割UI要求
                ui_parts = []
                if "- " in ui_requirements:
                    ui_parts = ui_requirements.split("- ")
                    ui_requirements = "\\n".join([f"- {part.strip()}" for part in ui_parts if part.strip()])
                elif "。" in ui_requirements:
                    ui_parts = ui_requirements.split("。")
                    ui_requirements = "\\n".join([f"- {part.strip()}。" for part in ui_parts if part.strip()])
            
            result = {
                "role": gpt_data["role"].replace("{app_name}", app_name),
                "goal": gpt_data["goal"].replace("{variant_folder}", variant_folder),
                "function_output": function_output,  # 移除fixed_content，由前端处理
                "ui_requirements": ui_requirements
            }
            self.logger.info("模板格式化成功")
            return result
            
        except json.JSONDecodeError as e:
            # 如果JSON解析失败，使用正则表达式提取内容
            self.logger.warning(f"JSON解析失败，使用备用解析方法: {str(e)}")
            return self._parse_text_output(gpt_output, app_name, variant_folder, ui_color)
    
    def _parse_text_output(self, text: str, app_name: str, variant_folder: str, ui_color: str = "蓝色科技感") -> dict:
        """备用文本解析方法"""
        self.logger.info("使用正则表达式解析文本输出")
        
        # 尝试提取JSON中的各个字段
        role_match = re.search(r'"role"\s*:\s*"([^"]+)"', text)
        goal_match = re.search(r'"goal"\s*:\s*"([^"]+)"', text)
        
        # 提取功能模块
        module1_title_match = re.search(r'"function_module_1"\s*:.*?"title"\s*:\s*"([^"]+)"', text, re.DOTALL)
        module1_desc_match = re.search(r'"function_module_1"\s*:.*?"description"\s*:\s*"([^"]+)"', text, re.DOTALL)
        module1_example_match = re.search(r'"function_module_1"\s*:.*?"example"\s*:\s*"([^"]+)"', text, re.DOTALL)
        
        module2_title_match = re.search(r'"function_module_2"\s*:.*?"title"\s*:\s*"([^"]+)"', text, re.DOTALL)
        module2_desc_match = re.search(r'"function_module_2"\s*:.*?"description"\s*:\s*"([^"]+)"', text, re.DOTALL)
        module2_example_match = re.search(r'"function_module_2"\s*:.*?"example"\s*:\s*"([^"]+)"', text, re.DOTALL)
        
        ui_match = re.search(r'"ui_requirements"\s*:\s*"([^"]+)"', text)
        
        # 构建功能输出
        function_output = ""
        if module1_title_match and module1_desc_match and module1_example_match:
            function_output += f"{module1_title_match.group(1)}\n\n{module1_desc_match.group(1)}\n\n{module1_example_match.group(1)}\n\n"
        
        if module2_title_match and module2_desc_match and module2_example_match:
            function_output += f"{module2_title_match.group(1)}\n\n{module2_desc_match.group(1)}\n\n{module2_example_match.group(1)}"
        
        if not function_output:
            function_output = "解析失败，请重新生成"
        # 移除固定内容添加，由前端处理
        
        result = {
            "role": role_match.group(1).replace("{app_name}", app_name) if role_match else "",
            "goal": goal_match.group(1).replace("{variant_folder}", variant_folder) if goal_match else "",
            "function_output": function_output,
            "ui_requirements": ui_match.group(1).replace("{ui_color}", ui_color) if ui_match else ""
        }
        self.logger.warning("文本解析完成，可能不完整")
        return result