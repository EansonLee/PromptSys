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
        
        # 主题特定的固定内容映射
        self.theme_fixed_content = {
            'wifi': {
                'keywords': ['wifi', 'WiFi', 'WIFI', '网络', '信号', '热点', '连接'],
                'content': """
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
13. 都要真实数据，WiFi无信号，没WiFi、WiFi不可用，没信号直接展示无数据即可，不要生成、展示模拟数据
14. 不执行任务编译、测试、命令
15. 不需要生成readMe文档"""
            },
            'clean': {
                'keywords': ['清理', '清洁', '净化', '清除', '整理', '优化'],
                'content': """
### 权限说明：
- 不需敏感系统权限，所有数据来源于应用本地题库记录  
所有数据仅存于本地数据库（Room）

---

- 参考 @variant\\variant_clean190626\\src\\main\\java\\com\\variant\\notification\\ 中的数据库实现与写法
- 参考 @AppUsageSettingActivity.kt 中使用"KeyValueUtils"进行持久化存储
- 如需要跳转Dialog 参考 @LinkPermissionDialog.kt 
- 如需跳转 Activity 参考 @AppUsageSettingActivity.kt 
- 参考 @variant_clean190616/ 中数据库的实现与写法
不需要执测试命令进行测试

##任务执行完，最后打印**任务已经执行完成**"""
            },
            'big': {
                'keywords': ['大字版', '放大', '大字', '老年', '视力', '字体'],
                'content': """
### 5. 数据采集逻辑：

如需要跳转Dialog参考 @variant\\variant_big131091\\src\\main\\java\\com\\dodg\\diverg\\ChaoqingTipDialog.kt 


6. 权限说明：
参考 @/variant  中其他变体以及 @base\\src\\main\\java\\com\\ljh\\major\\base\\utils\\PermissionComplianceManager.kt 中的申请权限的方法修改;
当前变体，同一个权限使用同一个key

7. 参考 @variant_big131125 中数据库的使用方式，数据库存放在变体下即可
8. 参考 @variant\\variant_big131125\\src\\main\\java\\com\\big\\adapter\\NoteEventAdapter.kt 编写RecycleView 的 Adapter
9. 不需要执测试命令进行测试
##任务执行完，最后打印**任务已经执行完成**"""
            },
            'traffic': {
                'keywords': ['流量', '数据', '网络', '上网', '消耗'],
                'content': """
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
13. 都要真实数据，WiFi无信号，没WiFi、WiFi不可用，没信号直接展示无数据即可，不要生成、展示模拟数据
14. 不执行任务编译、测试、命令
15. 不需要生成readMe文档"""
            }
        }
        
        # 默认固定内容（向后兼容）
        self.default_fixed_content = """
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
        
    def _format_reference_file(self, reference_file: str) -> str:
        """格式化参考文件名，添加@前缀和.kt后缀"""
        if not reference_file or not reference_file.strip():
            return "@TrafficJourneyFragment.kt"
        
        reference_file = reference_file.strip()
        # 移除已存在的@前缀和.kt后缀
        if reference_file.startswith("@"):
            reference_file = reference_file[1:]
        if reference_file.endswith(".kt"):
            reference_file = reference_file[:-3]
        
        return f"@{reference_file}.kt"
    
    def _detect_theme_type(self, theme: str) -> str:
        """根据主题内容检测主题类型，返回相应的固定内容"""
        theme_lower = theme.lower()
        
        # 检查每个主题类型的关键词
        for theme_type, config in self.theme_fixed_content.items():
            for keyword in config['keywords']:
                if keyword.lower() in theme_lower:
                    self.logger.info(f"检测到主题类型: {theme_type}，关键词: {keyword}")
                    return theme_type
        
        self.logger.info("未检测到特定主题类型，使用默认固定内容")
        return 'default'
    
    def _get_fixed_content(self, theme: str) -> str:
        """根据主题获取相应的固定内容"""
        theme_type = self._detect_theme_type(theme)
        
        if theme_type in self.theme_fixed_content:
            return self.theme_fixed_content[theme_type]['content']
        else:
            return self.default_fixed_content

    async def generate(self, theme: str, app_name: str, variant_folder: str, ui_color: str = "蓝色科技感", reference_file: str = "") -> str:
        """调用 GPT 生成提示词内容"""
        self.logger.info(f"开始生成提示词 - 主题: {theme[:30]}..., APP: {app_name}")
        
        # 格式化参考文件
        formatted_reference_file = self._format_reference_file(reference_file)
        self.logger.info(f"格式化参考文件: '{reference_file}' -> '{formatted_reference_file}'")
        
        system_prompt = """你是一位极具创意的 Android 开发工程师和提示词专家，擅长设计创新性、趣味性的移动应用功能。
根据用户输入的主题，生成一个充满创意和想象力的、带有两个创新小功能的 Fragment 设计文档。

【重要】：你只需要输出创意功能设计部分，不要包含任何技术实现细节、权限说明、数据库使用方法等内容。

输出格式要求：
```
角色：你是一位 Android 工具类 App 的创意开发工程师，目标是在「[APP名称]」中新增一个名为"[Fragment名称]"的 Fragment，[创意描述和功能概述]。

目标：
参考 {reference_file} 在 @{variant_folder}/ 变体下，构建一个以"[主题关键词]"为创意主题的 Fragment 页面，包含 2 个小功能模块：[模块1名称] + [模块2名称]，[数据处理方式说明]。

功能输出：
### 🔹 模块 1：[模块名称]（[功能类型]）
- [详细的用户交互描述和创意亮点]  
- [数据来源的概念描述，不涉及具体技术实现]  
- [视觉效果和动画的创意描述]  
- [用户体验和反馈机制描述]  
- [创意亮点和特色功能描述]  

**示例展示：**  
📅 [具体的使用场景，包含日期时间]  
✨ 动画：[详细的动画效果描述]  
🌌 [界面展示：具体的UI布局和内容展示]  

---

### 🔹 模块 2：[模块名称]（[功能类型]）
- [详细的用户交互描述和创意亮点]  
- [数据存储和检索的概念描述，不涉及具体技术实现]  
- [界面展示和布局设计描述]  
- [与模块1的联动或差异化描述]  
- [长期使用价值和用户粘性描述]  

**示例展示：**  
📚 [数据展示格式，包含具体示例]：  
- [示例数据条目1]  
- [示例数据条目2]  
- [示例数据条目3]  

📌 点击"[某个元素]" → [详细的交互反馈描述]  

UI 要求：
- 背景主色调：[具体颜色] {ui_color}，[风格描述]  
- [UI元素1]：[具体的颜色值] (#[色值1] / #[色值2])  
- 动画：[动画类型]、[效果描述]、[实现方式]  
- [界面布局]：[详细的布局描述和交互方式]  
- 所有控件使用原生 Android 控件，不使用 Material Design
```

创意要求：
1. 专注于创意功能设计，不涉及技术实现细节
2. 功能设计必须严格围绕用户输入的主题进行
3. 必须包含完整的两个功能模块，每个都有独特创意
4. 融入游戏化、可视化或个性化等创意元素
5. 使用生动有趣的比喻和场景描述
6. 包含详细的数据示例和交互反馈
7. UI描述要具体，包含颜色、动画效果
8. 避免提及具体的Android技术实现、权限申请、数据库使用等内容"""

        user_prompt = f"""主题：{theme}
APP名称：{app_name}
变体文件夹：{variant_folder}
UI主色调：{ui_color}
参考文件：{formatted_reference_file}

【重要】请严格按照以下结构输出，每个部分必须包含内容：

角色：[在这里写角色描述]

目标：[在这里写目标描述]

功能输出：
[在这里写两个模块的详细功能描述]

UI要求：
[在这里写UI设计要求]

【关键要求】：
1. 必须包含上述四个部分，每部分都要有实际内容
2. 功能设计必须严格围绕主题"{theme}"进行
3. 只描述创意功能和用户体验，不涉及技术实现
4. 融入游戏化、可视化等创意元素
5. 每个模块都要包含具体的示例展示

请确保严格按照格式输出，不要遗漏任何部分。"""

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
    
    def format_template(self, gpt_output: str, app_name: str, variant_folder: str, ui_color: str = "蓝色科技感", theme: str = "", reference_file: str = "") -> dict:
        """将GPT输出格式化为模板结构（现在是narrative格式，不再是JSON）"""
        self.logger.info("开始解析GPT的narrative格式输出并格式化为模板")
        
        try:
            # 清理输出中的控制字符
            cleaned_output = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', gpt_output)
            
            # 添加调试日志，输出GPT的原始返回内容
            self.logger.info(f"GPT原始输出内容预览: {cleaned_output[:500]}...")
            self.logger.info(f"GPT输出是否包含'角色：': {'角色：' in cleaned_output}")
            self.logger.info(f"GPT输出是否包含'目标：': {'目标：' in cleaned_output}")
            self.logger.info(f"GPT输出是否包含'功能输出：': {'功能输出：' in cleaned_output}")
            self.logger.info(f"GPT输出是否包含'UI要求：': {'UI要求：' in cleaned_output or 'UI 要求：' in cleaned_output}")
            
            # 使用更宽松的正则表达式解析narrative格式的内容
            # 匹配角色（从"角色："开始到"目标："之前，允许各种空白字符）
            role_match = re.search(r'角色：\s*(.*?)(?=目标：)', cleaned_output, re.DOTALL)
            
            # 匹配目标（从"目标："开始到"功能输出："之前）
            goal_match = re.search(r'目标：\s*(.*?)(?=功能输出：)', cleaned_output, re.DOTALL)
            
            # 提取功能模块内容（从"功能输出："开始到"UI要求："之前，允许有无空格）
            function_content_match = re.search(r'功能输出：\s*(.*?)(?=UI\s*要求：)', cleaned_output, re.DOTALL)
            
            # 提取UI要求（从"UI要求："开始，到固定内容之前）
            ui_match = re.search(r'UI\s*要求：\s*(.*?)(?=\n\s*###|权限说明：|数据采集逻辑：|$)', cleaned_output, re.DOTALL)
            
            # 构建结果
            role = role_match.group(1).strip() if role_match else ""
            goal = goal_match.group(1).strip() if goal_match else ""
            function_output = function_content_match.group(1).strip() if function_content_match else ""
            ui_requirements = ui_match.group(1).strip() if ui_match else ""
            
            # 清理目标内容中可能包含的功能输出内容
            if goal and '功能输出：' in goal:
                goal = re.sub(r'功能输出：.*$', '', goal, flags=re.DOTALL).strip()
                self.logger.warning("从目标内容中移除了功能输出部分")
            
            # 清理目标内容中可能包含的模块描述
            if goal and '### 🔹 模块' in goal:
                goal = re.sub(r'### 🔹 模块.*$', '', goal, flags=re.DOTALL).strip()
                self.logger.warning("从目标内容中移除了模块描述部分")
            
            # 格式化功能输出，确保正确的分行格式
            if function_output:
                # 先查找所有模块，确保不丢失任何模块
                all_modules = list(re.finditer(r'###?\s*🔹?\s*模块\s*\d+', function_output))
                self.logger.info(f"在原始内容中找到 {len(all_modules)} 个模块")
                
                # 如果找到模块，记录每个模块的位置和内容预览
                for i, module in enumerate(all_modules):
                    module_text = function_output[module.start():module.start()+50].replace('\n', ' ')
                    self.logger.info(f"模块 {i+1}: 位置 {module.start()}, 内容预览: {module_text}")
                
                # 移除开头的多余符号，但要保持模块内容完整
                # 先找到第一个模块的位置
                if all_modules:
                    # 如果有模块，从第一个模块开始保留内容
                    first_module_start = all_modules[0].start()
                    function_output = function_output[first_module_start:]
                    self.logger.info(f"从第一个模块（位置 {first_module_start}）开始保留内容")
                else:
                    # 如果没找到标准格式，尝试更宽松的匹配
                    first_module = re.search(r'模块\s*\d+', function_output)
                    if first_module:
                        function_output = function_output[first_module.start():]
                        self.logger.info("使用宽松匹配找到模块开始位置")
                    else:
                        # 如果完全没找到模块标记，只清理开头的符号但保留内容
                        function_output = re.sub(r'^[\s#]*\n*', '', function_output.strip())
                        self.logger.warning("没有找到任何模块标记，仅清理开头符号")
                
                # 重新验证清理后还有多少个模块
                remaining_modules = list(re.finditer(r'###?\s*🔹?\s*模块\s*\d+', function_output))
                self.logger.info(f"清理后保留了 {len(remaining_modules)} 个模块")
                
                # 确保每个"- "开头的要点分行显示
                function_output = re.sub(r'([^\n])\s*-\s+([^-])', r'\1\n- \2', function_output)
                
                # 确保模块标题前有适当换行
                function_output = re.sub(r'([^\n])(###?\s*🔹?\s*模块)', r'\1\n\n\2', function_output)
                
                # 确保模块之间的"---"前后有换行
                function_output = re.sub(r'([^\n])(\s*---\s*)([^\n])', r'\1\n\n\2\n\n\3', function_output)
                
                # 强化示例展示格式化
                # 1. 确保"**示例展示：**"独占一行
                function_output = re.sub(r'(\*\*示例展示：\*\*)\s*([^\n])', r'\1\n\2', function_output)
                
                # 2. 确保每个emoji都从新行开始
                for emoji in ['📅', '✨', '🌌', '📚', '📌']:
                    function_output = re.sub(rf'([^\n])\s*({emoji})', r'\1\n\2', function_output)
                
                # 3. 处理数据列表格式 (📚 开头的部分)
                # 确保列表项换行: - 项目1\n- 项目2
                function_output = re.sub(r'(📚[^📌\n]*?：)\s*-\s*([^-\n])', r'\1\n- \2', function_output)
                # 确保多个列表项之间换行
                function_output = re.sub(r'([^-\n])\s*-\s*([^-])', r'\1\n- \2', function_output)
                
                # 4. 处理点击操作格式 (📌 开头的部分)
                # 确保 → 符号换行
                function_output = re.sub(r'(📌[^→\n]*?)\s*(→)', r'\1\n\2', function_output)
                
                # 移除末尾可能的UI要求内容
                function_output = re.sub(r'\n\s*UI\s*要求：.*$', '', function_output, flags=re.DOTALL)
                
                # 清理开头多余的换行和分隔符
                function_output = re.sub(r'^[\s\n\-]+', '', function_output.strip())
                
                # 清理多余的连续换行符，但保留必要的双换行
                function_output = re.sub(r'\n\n\n+', '\n\n', function_output.strip())
            
            # 格式化UI要求并替换{ui_color}占位符
            if ui_requirements:
                # 替换{ui_color}占位符
                ui_requirements = ui_requirements.replace('{ui_color}', ui_color)
                # 确保每个"- "开头的项目分行
                ui_requirements = re.sub(r'(\s*)- ([^-])', r'\n\1- \2', ui_requirements)
                # 清理多余的换行符
                ui_requirements = re.sub(r'\n\n+', '\n\n', ui_requirements.strip())
            
            # 检查是否出现了内容耦合问题，如果function_output包含了角色、目标或UI要求
            if function_output and ('角色：' in function_output or '目标：' in function_output or 'UI 要求：' in function_output):
                self.logger.warning("检测到function_output中包含其他字段内容，进行内容清理...")
                
                # 如果function_output中包含角色，无论role字段是否为空都要从function_output中移除
                if '角色：' in function_output:
                    role_in_func = re.search(r'角色：(.*?)(?=目标：|---)', function_output, re.DOTALL)
                    if role_in_func:
                        if not role:  # 只有当role字段为空时才提取
                            role = role_in_func.group(1).strip()
                        function_output = function_output.replace(role_in_func.group(0), '').strip()
                
                # 如果function_output中包含目标，无论goal字段是否为空都要从function_output中移除
                if '目标：' in function_output:
                    goal_in_func = re.search(r'目标：(.*?)(?=---|###)', function_output, re.DOTALL)
                    if goal_in_func:
                        if not goal:  # 只有当goal字段为空时才提取
                            goal = goal_in_func.group(1).strip()
                        function_output = function_output.replace(goal_in_func.group(0), '').strip()
                
                # 如果function_output中包含UI要求，无论ui_requirements字段是否为空都要从function_output中移除
                if 'UI 要求：' in function_output:
                    ui_in_func = re.search(r'###?\s*UI\s*要求：(.*?)(?=###?\s*[\d\.]|权限说明：|$)', function_output, re.DOTALL)
                    if ui_in_func:
                        if not ui_requirements:  # 只有当ui_requirements字段为空时才提取
                            ui_requirements = ui_in_func.group(1).strip()
                        function_output = function_output.replace(ui_in_func.group(0), '').strip()
                
                # 清理function_output开头的多余分隔符和空白
                function_output = re.sub(r'^[\s\-\n]+', '', function_output).strip()
                
                # 如果清理后function_output只剩下分隔符和空白，确保从第一个模块开始
                if re.match(r'^[\s\-]*$', function_output):
                    function_output = ""
                
            # 如果任一字段解析失败，尝试增强解析
            if not role or not function_output:
                self.logger.warning("主要解析失败，尝试增强解析逻辑...")
                
                # 尝试更宽松的角色匹配
                if not role:
                    role_patterns = [
                        r'角色：\s*(.*?)(?=目标：|功能输出：|UI)',
                        r'你是一位.*?工程师.*?(?=目标：|功能输出：|\n)',
                        r'角色：\s*(.*?)(?=\n\n|\n目标)',
                    ]
                    for pattern in role_patterns:
                        role_match = re.search(pattern, cleaned_output, re.DOTALL)
                        if role_match:
                            role = role_match.group(1).strip()
                            self.logger.info(f"通过增强模式匹配到角色: {role[:50]}...")
                            break
                
                # 尝试更宽松的功能输出匹配
                if not function_output:
                    function_patterns = [
                        r'功能输出：\s*(.*?)(?=UI|### |\n\n### |\n权限|$)',
                        r'### 🔹.*?模块.*?(?=UI|权限|$)',
                        r'模块.*?：.*?(?=UI|权限|$)',
                    ]
                    for pattern in function_patterns:
                        function_match = re.search(pattern, cleaned_output, re.DOTALL)
                        if function_match:
                            function_output = function_match.group(0 if '模块' in pattern else 1).strip()
                            self.logger.info(f"通过增强模式匹配到功能输出: {function_output[:50]}...")
                            break
            
            # 特殊处理：如果内容全部耦合在一起，尝试分离
            elif not role and not goal and not function_output and not ui_requirements:
                self.logger.warning("所有内容可能耦合在一起，尝试分离...")
                
                # 尝试从整个输出中分离角色
                role_pattern = re.search(r'角色：(.*?)(?=目标：)', cleaned_output, re.DOTALL)
                if role_pattern:
                    role = role_pattern.group(1).strip()
                
                # 尝试分离目标
                goal_pattern = re.search(r'目标：(.*?)(?=---)', cleaned_output, re.DOTALL)  
                if goal_pattern:
                    goal = goal_pattern.group(1).strip()
                
                # 尝试分离功能模块部分（从"功能输出："到"UI要求："之间的内容）
                function_pattern = re.search(r'功能输出：(.*?)(?=UI\s*要求：)', cleaned_output, re.DOTALL)
                if function_pattern:
                    function_output = function_pattern.group(1).strip()
                    
                # 尝试分离UI要求部分
                ui_pattern = re.search(r'###?\s*UI\s*要求：(.*?)(?=###?\s*[\d\.]|权限说明：|$)', cleaned_output, re.DOTALL)
                if ui_pattern:
                    ui_requirements = ui_pattern.group(1).strip()
            
            # 如果没有找到结构化内容，尝试从整个内容中智能提取
            if not role and not goal:
                self.logger.warning("未找到标准的narrative结构，尝试智能解析")
                # 尝试找到任何"你是"或"角色"的描述作为角色
                role_fallback = re.search(r'(你是.*?工程师.*?)(?=\n|。)', cleaned_output)
                if role_fallback:
                    role = role_fallback.group(1).strip()
                else:
                    role = f"你是一位 Android 工具类 App 的创意开发工程师"
                    
                # 尝试找到任何"构建"或"目标"的描述作为目标
                goal_fallback = re.search(r'(构建.*?Fragment.*?)(?=\n|。)', cleaned_output)
                if goal_fallback:
                    goal = goal_fallback.group(1).strip()
                else:
                    goal = f"构建一个创意型 Fragment 页面"
                    
                # 如果还是没有找到功能输出，使用整个输出
                if not function_output:
                    function_output = cleaned_output
            
            # 获取主题对应的固定内容
            fixed_content = self._get_fixed_content(theme)
            self.logger.info(f"为主题 '{theme}' 选择了对应的固定内容")
            
            result = {
                "role": role,
                "goal": goal,
                "function_output": function_output,
                "ui_requirements": ui_requirements,
                "fixed_content": fixed_content,  # 新增：主题特定的固定内容
                "theme_type": self._detect_theme_type(theme)  # 新增：检测到的主题类型
            }
            
            self.logger.info("Narrative格式模板格式化成功")
            return result
            
        except Exception as e:
            self.logger.error(f"解析narrative格式输出时发生错误: {str(e)}")
            # 如果解析失败，返回基本结构
            fixed_content = self._get_fixed_content(theme)
            return {
                "role": f"你是一位 Android 工具类 App 的创意开发工程师",
                "goal": f"构建一个创意型 Fragment 页面",
                "function_output": cleaned_output,
                "ui_requirements": "",
                "fixed_content": fixed_content,
                "theme_type": self._detect_theme_type(theme)
            }
    
    def _parse_text_output(self, text: str, app_name: str, variant_folder: str, ui_color: str = "蓝色科技感", theme: str = "", reference_file: str = "") -> dict:
        """备用文本解析方法（已更新为处理narrative格式）"""
        self.logger.info("使用备用方法解析narrative格式输出")
        
        # 获取主题对应的固定内容
        fixed_content = self._get_fixed_content(theme)
        
        # 简单的文本解析，如果主要解析方法失败
        result = {
            "role": f"你是一位 Android 工具类 App 的创意开发工程师",
            "goal": f"构建一个创意型 Fragment 页面",
            "function_output": text,
            "ui_requirements": "",
            "fixed_content": fixed_content,
            "theme_type": self._detect_theme_type(theme)
        }
        
        self.logger.warning("备用文本解析完成，使用简化结构")
        return result