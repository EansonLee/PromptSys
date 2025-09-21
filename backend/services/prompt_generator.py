"""
Refactored prompt generator service using dependency injection.

This module serves as the main orchestrator for prompt generation,
using composition and dependency injection to coordinate between
specialized modules for theme configuration, LLM client management,
response parsing, and template building.
"""

import logging
from typing import Optional

from langchain.schema import HumanMessage, SystemMessage

from config import ThemeConfig
from clients import LLMClient
from parsers import ResponseParser
from templates import PromptTemplateBuilder, PromptContext


class PromptGenerator:
    """
    Main prompt generator service using dependency injection.
    
    This class orchestrates the prompt generation process by coordinating
    between specialized modules while maintaining the same public interface
    for backward compatibility.
    """
    
    def __init__(self, 
                 theme_config: Optional[ThemeConfig] = None,
                 llm_client: Optional[LLMClient] = None,
                 response_parser: Optional[ResponseParser] = None,
                 template_builder: Optional[PromptTemplateBuilder] = None):
        """
        Initialize prompt generator with dependency injection.
        
        Args:
            theme_config: Theme configuration manager
            llm_client: LLM client with dual strategy
            response_parser: Response parser for narrative format
            template_builder: Prompt template builder
        """
        self.logger = logging.getLogger(__name__)
        
        # Initialize dependencies (with defaults if not provided)
        self.theme_config = theme_config or ThemeConfig()
        self.llm_client = llm_client or LLMClient()
        self.response_parser = response_parser or ResponseParser()
        self.template_builder = template_builder or PromptTemplateBuilder()
        
        self.logger.info("PromptGenerator initialized with dependency injection")
        self.logger.info(f"Components: ThemeConfig={type(self.theme_config).__name__}, "
                        f"LLMClient={type(self.llm_client).__name__}, "
                        f"ResponseParser={type(self.response_parser).__name__}, "
                        f"TemplateBuilder={type(self.template_builder).__name__}")
    
    async def generate(self, theme: str, app_name: str, variant_folder: str,
                      ui_color: str = "蓝色科技感", reference_file: str = "",
                      prompt_type: str = "android") -> str:
        """
        Generate prompt content using LLM.

        This method maintains backward compatibility with the original interface
        while using the new modular architecture internally.

        Args:
            theme: Theme description
            app_name: Application name
            variant_folder: Variant folder name
            ui_color: UI color theme
            reference_file: Reference file name
            prompt_type: Type of prompt ("android" or "frontend")

        Returns:
            Generated prompt content from LLM
        """
        self.logger.info(f"Starting {prompt_type} prompt generation - theme: {theme[:30]}..., app: {app_name}")

        try:
            # Create prompt context
            context = self.template_builder.create_context(
                theme=theme,
                app_name=app_name,
                variant_folder=variant_folder,
                ui_color=ui_color,
                reference_file=reference_file
            )

            # Build prompts based on prompt type
            system_prompt = self.template_builder.build_system_prompt(prompt_type)
            user_prompt = self.template_builder.build_user_prompt(context, prompt_type)
            
            # Create message list
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            self.logger.info("=== Preparing LLM request ===")
            self.logger.info(f"System prompt length: {len(system_prompt)}")
            self.logger.info(f"User prompt length: {len(user_prompt)}")
            
            # Invoke LLM with dual strategy
            response_content = await self.llm_client.invoke(messages)
            
            self.logger.info("Prompt generation completed successfully")
            return response_content
            
        except Exception as e:
            self.logger.error(f"Error during prompt generation: {str(e)}")
            raise
    
    def format_template(self, gpt_output: str, app_name: str, variant_folder: str, 
                       ui_color: str = "蓝色科技感", theme: str = "", 
                       reference_file: str = "") -> dict:
        """
        Format GPT output into structured template.
        
        This method maintains backward compatibility with the original interface
        while using the new response parser internally.
        
        Args:
            gpt_output: Raw GPT output in narrative format
            app_name: Application name (for compatibility)
            variant_folder: Variant folder name (for compatibility)
            ui_color: UI color theme
            theme: Theme description
            reference_file: Reference file name (for compatibility)
            
        Returns:
            Dictionary with structured template components
        """
        self.logger.info("Starting template formatting with new parser")
        
        try:
            # Parse the response using the dedicated parser
            parsed_response = self.response_parser.parse_narrative_response(
                gpt_output=gpt_output,
                ui_color=ui_color
            )
            
            # Get theme-specific fixed content
            fixed_content = self.theme_config.get_fixed_content(theme)
            theme_type = self.theme_config.detect_theme_type(theme)
            
            # Build result dictionary maintaining original structure
            result = {
                "role": parsed_response.role,
                "goal": parsed_response.goal,
                "function_output": parsed_response.function_output,
                "ui_requirements": parsed_response.ui_requirements,
                "fixed_content": fixed_content,  # Theme-specific fixed content
                "theme_type": theme_type  # Detected theme type
            }
            
            self.logger.info(f"Template formatting completed successfully for theme type: {theme_type}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error during template formatting: {str(e)}")
            
            # Fallback structure to maintain compatibility
            fixed_content = self.theme_config.get_fixed_content(theme)
            theme_type = self.theme_config.detect_theme_type(theme)
            
            return {
                "role": "你是一位 Android 工具类 App 的创意开发工程师",
                "goal": "构建一个创意型 Fragment 页面",
                "function_output": gpt_output,
                "ui_requirements": "",
                "fixed_content": fixed_content,
                "theme_type": theme_type
            }
    
    # Legacy methods for backward compatibility (delegating to internal components)
    
    def _detect_theme_type(self, theme: str) -> str:
        """Legacy method for theme detection (delegates to ThemeConfig)."""
        return self.theme_config.detect_theme_type(theme)
    
    def _get_fixed_content(self, theme: str) -> str:
        """Legacy method for fixed content (delegates to ThemeConfig)."""
        return self.theme_config.get_fixed_content(theme)
    
    def _format_reference_file(self, reference_file: str) -> str:
        """Legacy method for reference file formatting (delegates to TemplateBuilder)."""
        return self.template_builder.format_reference_file(reference_file)
    
    def _parse_text_output(self, text: str, app_name: str, variant_folder: str, 
                          ui_color: str = "蓝色科技感", theme: str = "", 
                          reference_file: str = "") -> dict:
        """
        Legacy backup text parsing method.
        
        This method maintains backward compatibility while using the new parser.
        """
        self.logger.info("Using legacy backup text parsing method")
        
        # Use the new parser for backup parsing
        parsed_response = self.response_parser.parse_narrative_response(
            gpt_output=text,
            ui_color=ui_color
        )
        
        # Get theme-specific content
        fixed_content = self.theme_config.get_fixed_content(theme)
        theme_type = self.theme_config.detect_theme_type(theme)
        
        result = {
            "role": parsed_response.role or "你是一位 Android 工具类 App 的创意开发工程师",
            "goal": parsed_response.goal or "构建一个创意型 Fragment 页面", 
            "function_output": parsed_response.function_output or text,
            "ui_requirements": parsed_response.ui_requirements,
            "fixed_content": fixed_content,
            "theme_type": theme_type
        }
        
        self.logger.warning("Legacy backup parsing completed, using simplified structure")
        return result
    
    # Utility methods for inspecting the injected dependencies
    
    def get_component_info(self) -> dict:
        """
        Get information about injected components.
        
        Returns:
            Dictionary with component information
        """
        return {
            "theme_config": {
                "type": type(self.theme_config).__name__,
                "available_themes": self.theme_config.get_available_themes()
            },
            "llm_client": {
                "type": type(self.llm_client).__name__,
                "primary_model": self.llm_client.get_primary_model_info(),
                "fallback_model": self.llm_client.get_fallback_model_info()
            },
            "response_parser": {
                "type": type(self.response_parser).__name__
            },
            "template_builder": {
                "type": type(self.template_builder).__name__,
                "template_info": self.template_builder.get_template_info()
            }
        }
    
    def validate_configuration(self) -> dict:
        """
        Validate that all components are properly configured.
        
        Returns:
            Dictionary with validation results
        """
        validation_results = {
            "theme_config": True,
            "llm_client": False,
            "response_parser": True,
            "template_builder": False
        }
        
        issues = []
        
        # Validate LLM client
        primary_info = self.llm_client.get_primary_model_info()
        fallback_info = self.llm_client.get_fallback_model_info()
        
        if not primary_info.get("has_api_key"):
            issues.append("Primary LLM missing API key")
        else:
            validation_results["llm_client"] = True
            
        if not fallback_info.get("has_api_key"):
            issues.append("Fallback LLM missing API key")
        
        # Validate template builder
        template_info = self.template_builder.get_template_info()
        if template_info.get("has_system_prompt") and template_info.get("has_user_prompt_template"):
            validation_results["template_builder"] = True
        else:
            issues.append("Template builder missing templates")
        
        return {
            "valid": all(validation_results.values()),
            "component_status": validation_results,
            "issues": issues
        }