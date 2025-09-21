"""
Prompt template management module.

This module handles the creation and formatting of prompt templates
for LLM interactions, including system prompts, user prompts, and
reference file formatting.
"""

import logging
from typing import Optional
from dataclasses import dataclass


@dataclass
class PromptContext:
    """Context data for prompt generation."""
    theme: str
    app_name: str
    variant_folder: str
    ui_color: str
    reference_file: str


class PromptTemplateBuilder:
    """
    Builds and manages prompt templates for LLM interactions.
    
    This class handles the creation of system and user prompts,
    reference file formatting, and template customization.
    """
    
    def __init__(self):
        """Initialize prompt template builder."""
        self.logger = logging.getLogger(__name__)

        # Android system and user prompt templates
        self._android_system_prompt_template = self._get_android_system_prompt_template()
        self._android_user_prompt_template = self._get_android_user_prompt_template()

        # Frontend system and user prompt templates
        self._frontend_system_prompt_template = self._get_frontend_system_prompt_template()
        self._frontend_user_prompt_template = self._get_frontend_user_prompt_template()

        self.logger.info("PromptTemplateBuilder initialized with Android and Frontend templates")
    
    def _get_android_system_prompt_template(self) -> str:
        """Get the Android system prompt template."""
        return """你是一位极具创意的 Android 开发工程师和提示词专家，擅长设计创新性、趣味性的移动应用功能。
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
    
    def _get_android_user_prompt_template(self) -> str:
        """Get the Android user prompt template."""
        return """主题：{theme}
APP名称：{app_name}
变体文件夹：{variant_folder}
UI主色调：{ui_color}
参考文件：{reference_file}

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

    def _get_frontend_system_prompt_template(self) -> str:
        """Get the Frontend system prompt template."""
        return """你是一位极具创意的前端开发工程师和用户体验专家，擅长设计现代化、响应式的Web应用组件和界面。
根据用户输入的主题，生成一个充满创意和想象力的、包含两个创新功能模块的前端组件设计文档。

【重要】：你只需要输出创意功能设计部分，不要包含任何技术实现细节、代码片段、框架选择等内容。

输出格式要求：
```
角色：你是一位现代化前端应用的创意设计师，目标是在「[项目名称]」中新增一个名为"[组件名称]"的React组件，[创意描述和功能概述]。

目标：
参考 {reference_file} 在 @{variant_folder}/ 组件目录下，构建一个以"[主题关键词]"为创意主题的前端组件，包含 2 个功能模块：[模块1名称] + [模块2名称]，[数据处理和交互方式说明]。

功能输出：
### 🔹 模块 1：[模块名称]（[功能类型]）
- [详细的用户交互描述和创意亮点]
- [数据来源和处理的概念描述，不涉及具体技术实现]
- [视觉效果、动画和响应式设计的创意描述]
- [用户体验和反馈机制描述]
- [创意亮点和特色功能描述]

**示例展示：**
📅 [具体的使用场景，包含用户操作流程]
✨ 动画：[详细的交互动画效果描述]
🌌 [界面展示：具体的布局、卡片设计和内容展示]

---

### 🔹 模块 2：[模块名称]（[功能类型]）
- [详细的用户交互描述和创意亮点]
- [数据存储和状态管理的概念描述，不涉及具体技术实现]
- [界面展示和响应式布局设计描述]
- [与模块1的联动或差异化描述]
- [长期使用价值和用户粘性描述]

**示例展示：**
📚 [数据展示格式，包含具体示例]：
- [示例数据条目1]
- [示例数据条目2]
- [示例数据条目3]

📌 点击"[某个元素]" → [详细的交互反馈和页面跳转描述]

UI 要求：
- 主色调：[具体颜色] {ui_color}，[现代化设计风格描述]
- [UI元素1]：[具体的颜色值] (#[色值1] / #[色值2])
- 动画：[动画类型]、[效果描述]、[交互方式]
- [响应式布局]：[详细的桌面端、平板、手机端适配描述]
- 使用现代化设计语言，支持深色/浅色主题切换
```

创意要求：
1. 专注于前端组件设计，不涉及后端技术实现细节
2. 功能设计必须严格围绕用户输入的主题进行
3. 必须包含完整的两个功能模块，每个都有独特的前端特色
4. 融入现代化UI/UX设计理念、微交互、响应式设计等元素
5. 使用生动有趣的比喻和场景描述
6. 包含详细的交互示例和用户反馈
7. UI描述要具体，包含颜色、动画效果、响应式适配
8. 避免提及具体的前端框架实现、API调用、状态管理库使用等内容"""

    def _get_frontend_user_prompt_template(self) -> str:
        """Get the Frontend user prompt template."""
        return """主题：{theme}
项目名称：{app_name}
组件目录：{variant_folder}
UI主色调：{ui_color}
参考组件：{reference_file}

【重要】请严格按照以下结构输出，每个部分必须包含内容：

角色：[在这里写前端设计师角色描述]

目标：[在这里写组件设计目标描述]

功能输出：
[在这里写两个模块的详细功能设计描述]

UI要求：
[在这里写现代化前端UI设计要求]

【关键要求】：
1. 必须包含上述四个部分，每部分都要有实际内容
2. 功能设计必须严格围绕主题"{theme}"进行
3. 只描述前端组件创意功能和用户体验，不涉及技术实现
4. 融入现代化前端设计理念、微交互、响应式设计等元素
5. 每个模块都要包含具体的交互示例展示
6. 重点描述用户界面、交互动画和响应式适配

请确保严格按照格式输出，不要遗漏任何部分。"""
    
    def format_reference_file(self, reference_file: str) -> str:
        """
        Format reference file name with proper prefix and suffix.
        
        Args:
            reference_file: Raw reference file name
            
        Returns:
            Formatted reference file name with @prefix and .kt suffix
        """
        if not reference_file or not reference_file.strip():
            return "@TrafficJourneyFragment.kt"
        
        reference_file = reference_file.strip()
        
        # Remove existing @prefix and .kt suffix
        if reference_file.startswith("@"):
            reference_file = reference_file[1:]
        if reference_file.endswith(".kt"):
            reference_file = reference_file[:-3]
        
        formatted = f"@{reference_file}.kt"
        self.logger.info(f"Formatted reference file: '{reference_file}' -> '{formatted}'")
        return formatted
    
    def build_system_prompt(self, prompt_type: str = "android") -> str:
        """
        Build the system prompt based on prompt type.

        Args:
            prompt_type: Type of prompt ("android" or "frontend")

        Returns:
            The system prompt string
        """
        if prompt_type == "frontend":
            return self._frontend_system_prompt_template
        else:
            return self._android_system_prompt_template
    
    def build_user_prompt(self, context: PromptContext, prompt_type: str = "android") -> str:
        """
        Build the user prompt with context substitution based on prompt type.

        Args:
            context: Prompt context with theme, app name, etc.
            prompt_type: Type of prompt ("android" or "frontend")

        Returns:
            The user prompt string with substituted values
        """
        # Format reference file
        formatted_reference_file = self.format_reference_file(context.reference_file)

        # Choose template based on prompt type
        if prompt_type == "frontend":
            template = self._frontend_user_prompt_template
        else:
            template = self._android_user_prompt_template

        # Substitute template variables
        user_prompt = template.format(
            theme=context.theme,
            app_name=context.app_name,
            variant_folder=context.variant_folder,
            ui_color=context.ui_color,
            reference_file=formatted_reference_file
        )

        self.logger.info(f"Built {prompt_type} user prompt for theme: {context.theme[:30]}..., app: {context.app_name}")
        self.logger.info(f"User prompt length: {len(user_prompt)}")

        return user_prompt
    
    def get_template_info(self) -> dict:
        """
        Get information about all available templates.

        Returns:
            Dictionary with template information
        """
        return {
            "android": {
                "system_prompt_length": len(self._android_system_prompt_template),
                "user_prompt_template_length": len(self._android_user_prompt_template),
                "has_system_prompt": bool(self._android_system_prompt_template),
                "has_user_prompt_template": bool(self._android_user_prompt_template)
            },
            "frontend": {
                "system_prompt_length": len(self._frontend_system_prompt_template),
                "user_prompt_template_length": len(self._frontend_user_prompt_template),
                "has_system_prompt": bool(self._frontend_system_prompt_template),
                "has_user_prompt_template": bool(self._frontend_user_prompt_template)
            },
            # Legacy fields for backward compatibility
            "has_system_prompt": True,
            "has_user_prompt_template": True
        }
    
    def validate_context(self, context: PromptContext) -> bool:
        """
        Validate that prompt context has required fields.
        
        Args:
            context: Prompt context to validate
            
        Returns:
            True if context is valid, False otherwise
        """
        required_fields = ['theme', 'app_name', 'variant_folder']
        missing_fields = []
        
        for field in required_fields:
            if not getattr(context, field, None):
                missing_fields.append(field)
        
        if missing_fields:
            self.logger.error(f"Missing required context fields: {missing_fields}")
            return False
        
        return True
    
    def create_context(self, theme: str, app_name: str, variant_folder: str, 
                      ui_color: str = "蓝色科技感", reference_file: str = "") -> PromptContext:
        """
        Create a prompt context with validation.
        
        Args:
            theme: Theme description
            app_name: Application name
            variant_folder: Variant folder name
            ui_color: UI color theme
            reference_file: Reference file name
            
        Returns:
            PromptContext object
            
        Raises:
            ValueError: If required fields are missing
        """
        context = PromptContext(
            theme=theme,
            app_name=app_name,
            variant_folder=variant_folder,
            ui_color=ui_color or "蓝色科技感",
            reference_file=reference_file
        )
        
        if not self.validate_context(context):
            raise ValueError("Invalid prompt context: missing required fields")
        
        return context