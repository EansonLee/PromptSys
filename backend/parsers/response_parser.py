"""
Response parser module for handling complex narrative format parsing.

This module extracts the complex parsing logic from the monolithic prompt
generator and provides structured parsing capabilities for LLM responses.
"""

import re
import logging
from typing import Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class ParsedResponse:
    """Data class representing a parsed LLM response."""
    role: str
    goal: str
    function_output: str
    ui_requirements: str
    raw_content: str


class ResponseParser:
    """
    Handles complex parsing of narrative format LLM responses.
    
    This class extracts role, goal, function output, and UI requirements
    from structured narrative responses using sophisticated regex patterns
    and formatting rules.
    """
    
    def __init__(self):
        """Initialize response parser."""
        self.logger = logging.getLogger(__name__)
        
        # Emoji to text mapping for formatting
        self._emoji_patterns = {
            '📅': '日期：',
            '✨': '动画：',
            '🌌': '界面展示：',
            '📚': '数据展示格式：',
            '📌': '点击操作：'
        }
        
        # Text patterns for example formatting
        self._text_patterns = ['日期：', '动画：', '界面展示：', '数据展示格式：', '点击操作：']
        
        self.logger.info("ResponseParser initialized")
    
    def parse_narrative_response(self, gpt_output: str, ui_color: str = "蓝色科技感") -> ParsedResponse:
        """
        Parse narrative format GPT output into structured components.
        
        Args:
            gpt_output: Raw GPT output in narrative format
            ui_color: UI color theme to replace placeholders
            
        Returns:
            ParsedResponse object with extracted components
        """
        self.logger.info("Starting narrative format parsing")
        
        # Clean output of control characters
        cleaned_output = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', gpt_output)
        
        # Log parsing debug info
        self._log_parsing_debug_info(cleaned_output)
        
        # Extract structured components
        role = self._extract_role(cleaned_output)
        goal = self._extract_goal(cleaned_output)
        function_output = self._extract_function_output(cleaned_output)
        ui_requirements = self._extract_ui_requirements(cleaned_output, ui_color)
        
        # Apply content separation if needed
        role, goal, function_output, ui_requirements = self._separate_coupled_content(
            cleaned_output, role, goal, function_output, ui_requirements
        )
        
        # Enhanced parsing fallback if main parsing fails
        if not role or not function_output:
            self.logger.warning("Main parsing failed, attempting enhanced parsing...")
            role, goal, function_output, ui_requirements = self._enhanced_parsing(
                cleaned_output, role, goal, function_output, ui_requirements
            )
        
        # Format function output
        if function_output:
            function_output = self._format_function_output(function_output)
        
        # Format UI requirements
        if ui_requirements:
            ui_requirements = self._format_ui_requirements(ui_requirements, ui_color)
        
        # Final fallback for completely coupled content
        if not role and not goal and not function_output and not ui_requirements:
            self.logger.warning("All content appears coupled, attempting separation...")
            role, goal, function_output, ui_requirements = self._separate_fully_coupled_content(cleaned_output)
        
        # Smart fallback if no structured content found
        if not role and not goal:
            role, goal = self._smart_fallback_extraction(cleaned_output)
            if not function_output:
                function_output = cleaned_output
        
        result = ParsedResponse(
            role=role,
            goal=goal,
            function_output=function_output,
            ui_requirements=ui_requirements,
            raw_content=cleaned_output
        )
        
        self.logger.info("Narrative format parsing completed successfully")
        return result
    
    def _log_parsing_debug_info(self, cleaned_output: str) -> None:
        """Log debug information about the content to be parsed."""
        self.logger.info(f"GPT output preview: {cleaned_output[:500]}...")
        self.logger.info(f"Contains '角色：': {'角色：' in cleaned_output}")
        self.logger.info(f"Contains '目标：': {'目标：' in cleaned_output}")
        self.logger.info(f"Contains '功能输出：': {'功能输出：' in cleaned_output}")
        self.logger.info(f"Contains 'UI要求：': {'UI要求：' in cleaned_output or 'UI 要求：' in cleaned_output}")
    
    def _extract_role(self, content: str) -> str:
        """Extract role from narrative content."""
        role_match = re.search(r'角色：\s*(.*?)(?=目标：)', content, re.DOTALL)
        return role_match.group(1).strip() if role_match else ""
    
    def _extract_goal(self, content: str) -> str:
        """Extract goal from narrative content."""
        goal_match = re.search(r'目标：\s*(.*?)(?=功能输出：)', content, re.DOTALL)
        goal = goal_match.group(1).strip() if goal_match else ""
        
        # Clean goal content of any function output content
        if goal and '功能输出：' in goal:
            goal = re.sub(r'功能输出：.*$', '', goal, flags=re.DOTALL).strip()
            self.logger.warning("Removed function output content from goal")
        
        # Clean goal content of module descriptions
        if goal and '### 🔹 模块' in goal:
            goal = re.sub(r'### 🔹 模块.*$', '', goal, flags=re.DOTALL).strip()
            self.logger.warning("Removed module description from goal")
        
        return goal
    
    def _extract_function_output(self, content: str) -> str:
        """Extract function output from narrative content."""
        function_content_match = re.search(
            r'功能输出：\s*(.*?)(?=UI\s*要求：|权限说明：|数据采集逻辑：|###\s*\d+\.|$)', 
            content, re.DOTALL
        )
        return function_content_match.group(1).strip() if function_content_match else ""
    
    def _extract_ui_requirements(self, content: str, ui_color: str) -> str:
        """Extract UI requirements from narrative content."""
        ui_match = re.search(
            r'UI\s*要求：\s*(.*?)(?=\n\s*###|权限说明：|数据采集逻辑：|任务执行完|$)', 
            content, re.DOTALL
        )
        ui_requirements = ui_match.group(1).strip() if ui_match else ""
        
        # Replace {ui_color} placeholder
        if ui_requirements:
            ui_requirements = ui_requirements.replace('{ui_color}', ui_color)
        
        return ui_requirements
    
    def _separate_coupled_content(self, content: str, role: str, goal: str, 
                                function_output: str, ui_requirements: str) -> tuple:
        """Separate content that may be coupled together."""
        if not function_output:
            return role, goal, function_output, ui_requirements
        
        # Check if function_output contains other field content
        if any(field in function_output for field in ['角色：', '目标：', 'UI 要求：']):
            self.logger.warning("Detected coupled content in function_output, separating...")
            
            # Extract and remove role from function_output
            if '角色：' in function_output:
                role_in_func = re.search(r'角色：(.*?)(?=目标：|---)', function_output, re.DOTALL)
                if role_in_func:
                    if not role:  # Only extract if role field is empty
                        role = role_in_func.group(1).strip()
                    function_output = function_output.replace(role_in_func.group(0), '').strip()
            
            # Extract and remove goal from function_output
            if '目标：' in function_output:
                goal_in_func = re.search(r'目标：(.*?)(?=---|###)', function_output, re.DOTALL)
                if goal_in_func:
                    if not goal:  # Only extract if goal field is empty
                        goal = goal_in_func.group(1).strip()
                    function_output = function_output.replace(goal_in_func.group(0), '').strip()
            
            # Extract and remove UI requirements from function_output
            if 'UI 要求：' in function_output:
                ui_in_func = re.search(
                    r'###?\s*UI\s*要求：(.*?)(?=###?\s*[\d\.]|权限说明：|$)', 
                    function_output, re.DOTALL
                )
                if ui_in_func:
                    if not ui_requirements:  # Only extract if ui_requirements field is empty
                        ui_requirements = ui_in_func.group(1).strip()
                    function_output = function_output.replace(ui_in_func.group(0), '').strip()
            
            # Clean function_output of leading separators and whitespace
            function_output = re.sub(r'^[\s\-\n]+', '', function_output).strip()
            
            # If function_output is now empty, ensure we start from first module
            if re.match(r'^[\s\-]*$', function_output):
                function_output = ""
        
        return role, goal, function_output, ui_requirements
    
    def _enhanced_parsing(self, content: str, role: str, goal: str, 
                        function_output: str, ui_requirements: str) -> tuple:
        """Enhanced parsing logic with more flexible patterns."""
        # Try more flexible role matching
        if not role:
            role_patterns = [
                r'角色：\s*(.*?)(?=目标：|功能输出：|UI)',
                r'你是一位.*?工程师.*?(?=目标：|功能输出：|\n)',
                r'角色：\s*(.*?)(?=\n\n|\n目标)',
            ]
            for pattern in role_patterns:
                role_match = re.search(pattern, content, re.DOTALL)
                if role_match:
                    role = role_match.group(1).strip()
                    self.logger.info(f"Enhanced parsing matched role: {role[:50]}...")
                    break
        
        # Try more flexible function output matching
        if not function_output:
            function_patterns = [
                r'功能输出：\s*(.*?)(?=UI\s*要求：|权限说明：|数据采集逻辑：|任务执行完|$)',
                r'功能输出：\s*(.*?)(?=### \d+\.|$)',
                r'### 🔹.*?模块.*?(?=UI|权限|数据采集|任务执行|$)',
                r'模块\s*\d+.*?(?=UI|权限|数据采集|任务执行|$)',
            ]
            for pattern in function_patterns:
                function_match = re.search(pattern, content, re.DOTALL)
                if function_match:
                    function_output = function_match.group(0 if '模块' in pattern else 1).strip()
                    self.logger.info(f"Enhanced parsing matched function output: {function_output[:100]}...")
                    break
        
        return role, goal, function_output, ui_requirements
    
    def _separate_fully_coupled_content(self, content: str) -> tuple:
        """Attempt to separate fully coupled content."""
        self.logger.warning("Attempting to separate fully coupled content...")
        
        # Try to extract role
        role_pattern = re.search(r'角色：(.*?)(?=目标：)', content, re.DOTALL)
        role = role_pattern.group(1).strip() if role_pattern else ""
        
        # Try to extract goal
        goal_pattern = re.search(r'目标：(.*?)(?=---)', content, re.DOTALL)
        goal = goal_pattern.group(1).strip() if goal_pattern else ""
        
        # Try to extract function modules
        function_patterns = [
            r'功能输出：(.*?)(?=UI\s*要求：)',
            r'功能输出：(.*?)(?=权限说明：|数据采集逻辑：|任务执行完|###\s*\d+\.)',
            r'功能输出：(.*?)$',  # Fallback to end of document
        ]
        function_output = ""
        for pattern in function_patterns:
            function_pattern = re.search(pattern, content, re.DOTALL)
            if function_pattern:
                function_output = function_pattern.group(1).strip()
                self.logger.info(f"Extracted function output using pattern '{pattern}', length: {len(function_output)}")
                break
        
        # Try to extract UI requirements
        ui_pattern = re.search(r'###?\s*UI\s*要求：(.*?)(?=###?\s*[\d\.]|权限说明：|$)', content, re.DOTALL)
        ui_requirements = ui_pattern.group(1).strip() if ui_pattern else ""
        
        return role, goal, function_output, ui_requirements
    
    def _smart_fallback_extraction(self, content: str) -> tuple:
        """Smart fallback extraction for unstructured content."""
        self.logger.warning("Using smart fallback extraction for unstructured content")
        
        # Try to find any "你是" or "角色" description as role
        role_fallback = re.search(r'(你是.*?工程师.*?)(?=\n|。)', content)
        role = role_fallback.group(1).strip() if role_fallback else "你是一位 Android 工具类 App 的创意开发工程师"
        
        # Try to find any "构建" or "目标" description as goal
        goal_fallback = re.search(r'(构建.*?Fragment.*?)(?=\n|。)', content)
        goal = goal_fallback.group(1).strip() if goal_fallback else "构建一个创意型 Fragment 页面"
        
        return role, goal
    
    def _format_function_output(self, function_output: str) -> str:
        """Format function output with proper structure and emoji handling."""
        if not function_output:
            return function_output
        
        # Find and preserve all modules
        all_modules = list(re.finditer(r'###?\s*🔹?\s*模块\s*\d+', function_output))
        self.logger.info(f"Found {len(all_modules)} modules in function output")
        
        # Log each module position
        for i, module in enumerate(all_modules):
            module_text = function_output[module.start():module.start()+50].replace('\n', ' ')
            self.logger.info(f"Module {i+1}: position {module.start()}, preview: {module_text}")
        
        # Start from first module if found
        if all_modules:
            first_module_start = all_modules[0].start()
            function_output = function_output[first_module_start:]
            self.logger.info(f"Starting from first module at position {first_module_start}")
        
        # Verify remaining modules after cleaning
        remaining_modules = list(re.finditer(r'###?\s*🔹?\s*模块\s*\d+', function_output))
        self.logger.info(f"After cleaning, {len(remaining_modules)} modules remain")
        
        # Format bullet points
        function_output = re.sub(r'([^\n])\s*-\s+([^-])', r'\1\n- \2', function_output)
        
        # Format module titles
        function_output = re.sub(r'([^\n])(###?\s*🔹?\s*模块)', r'\1\n\n\2', function_output)
        
        # Format separators
        function_output = re.sub(r'([^\n])(\s*---\s*)([^\n])', r'\1\n\n\2\n\n\3', function_output)
        
        # Format example sections
        function_output = self._format_example_sections(function_output)
        
        # Remove UI requirements content from function output
        function_output = re.sub(r'\n\s*UI\s*要求：.*$', '', function_output, flags=re.DOTALL)
        
        # Clean leading separators and excessive newlines
        function_output = re.sub(r'^[\s\n\-]+', '', function_output.strip())
        function_output = re.sub(r'\n\n\n+', '\n\n', function_output.strip())
        
        return function_output
    
    def _format_example_sections(self, content: str) -> str:
        """Format example sections with proper structure."""
        # Ensure "**示例展示：**" is on its own line
        content = re.sub(r'([^\n])\s*(\*\*示例展示：\*\*)', r'\1\n\2', content)
        content = re.sub(r'(\*\*示例展示：\*\*)\s*([^\n\s])', r'\1\n\2', content)
        content = re.sub(r'(\*\*示例展示：\*\*)\s+([^\n])', r'\1\n\2', content)
        
        # Handle special date formats
        content = re.sub(r'📅\s*(\d{4})\s*-\s*(\d{1,2})\s*-\s*(\d{1,2})', r'日期： \1年\2月\3日', content)
        content = re.sub(r'📅\s*(\d{4})\n-\s*(\d{1,2})\n-\s*(\d{1,2})', r'日期： \1年\2月\3日', content)
        
        # Replace emojis with text
        for emoji, replacement in self._emoji_patterns.items():
            content = re.sub(rf'([^\n])\s*{re.escape(emoji)}', r'\1\n' + replacement, content)
            content = content.replace(emoji, replacement)
        
        # Format text patterns
        for pattern in self._text_patterns:
            content = re.sub(rf'([^\n])\s*({re.escape(pattern)})', r'\1\n\2', content)
            # Remove duplicate patterns
            content = re.sub(rf'{re.escape(pattern)}\s*{re.escape(pattern)}', pattern, content)
        
        # Format data lists
        content = re.sub(r'(数据展示格式：)\s*([^-\n])', r'\1\n- \2', content)
        content = re.sub(r'([^-\n])\s*-\s*([^-\n])', r'\1\n- \2', content)
        
        # Format click operations
        content = re.sub(r'(点击操作：[^→\n]*?)\s*(→)', r'\1\n\2', content)
        
        # Ensure different example types are separated
        for i in range(len(self._text_patterns) - 1):
            current = self._text_patterns[i]
            next_type = self._text_patterns[i + 1]
            content = re.sub(rf'({current}[^\n]*)\s+({next_type})', r'\1\n\2', content)
        
        # Final cleanup of example sections
        content = re.sub(r'([^\n])(\*\*示例展示：\*\*)', r'\1\n\2', content)
        content = re.sub(r'(\*\*示例展示：\*\*)([^\n])', r'\1\n\2', content)
        content = re.sub(r'(\*\*示例展示：\*\*\n)\n+', r'\1', content)
        
        # Remove remaining emojis
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "]+", flags=re.UNICODE)
        content = emoji_pattern.sub('', content)
        
        self.logger.info("Example sections formatted successfully")
        return content
    
    def _format_ui_requirements(self, ui_requirements: str, ui_color: str) -> str:
        """Format UI requirements content."""
        if not ui_requirements:
            return ui_requirements
        
        # Replace {ui_color} placeholder
        ui_requirements = ui_requirements.replace('{ui_color}', ui_color)
        
        # Ensure bullet points are properly formatted
        ui_requirements = re.sub(r'(\s*)- ([^-])', r'\n\1- \2', ui_requirements)
        
        # Clean excessive newlines
        ui_requirements = re.sub(r'\n\n+', '\n\n', ui_requirements.strip())
        
        return ui_requirements