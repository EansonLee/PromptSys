"""
LLM client management module with dual strategy support.

This module handles the configuration and management of multiple LLM clients
with a primary/fallback strategy for increased reliability.
"""

import os
import logging
from typing import Optional, List
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain.schema import BaseMessage


@dataclass
class LLMConfig:
    """Configuration data class for LLM settings."""
    api_key: str
    base_url: Optional[str] = None
    model: str = "gpt-4"
    temperature: float = 0.7


class LLMClient:
    """
    Manages LLM clients with primary and fallback strategy.
    
    This class provides a dual LLM strategy where if the primary LLM fails
    due to rate limits, quota issues, or server errors, it automatically
    falls back to a secondary LLM provider.
    """
    
    def __init__(self, primary_config: Optional[LLMConfig] = None, 
                 fallback_config: Optional[LLMConfig] = None):
        """
        Initialize LLM client with primary and fallback configurations.
        
        Args:
            primary_config: Primary LLM configuration
            fallback_config: Fallback LLM configuration
        """
        self.logger = logging.getLogger(__name__)
        
        # Configure detailed logging for HTTP clients
        self._configure_logging()
        
        # Initialize configurations
        self.primary_config = primary_config or self._get_primary_config()
        self.fallback_config = fallback_config or self._get_fallback_config()
        
        # Initialize LLM instances
        self.primary_llm = self._create_llm(self.primary_config)
        self.fallback_llm = self._create_llm(self.fallback_config)
        
        # Log configuration details
        self._log_configuration()
        
        self.logger.info("LLM client initialized successfully")
    
    def _configure_logging(self) -> None:
        """Configure detailed logging for LLM-related modules."""
        logging.getLogger("httpx").setLevel(logging.DEBUG)
        logging.getLogger("openai").setLevel(logging.DEBUG)
        logging.getLogger("langchain").setLevel(logging.DEBUG)
    
    def _get_primary_config(self) -> LLMConfig:
        """Get primary LLM configuration from environment variables."""
        return LLMConfig(
            api_key=os.getenv("OPENAI_API_KEY", ""),
            base_url=os.getenv("OPENAI_BASE_URL"),
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7"))
        )
    
    def _get_fallback_config(self) -> LLMConfig:
        """Get fallback LLM configuration from environment variables."""
        return LLMConfig(
            api_key=os.getenv("SILICONFLOW_API_KEY", "sk-dummy-key"),
            base_url=os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1"),
            model=os.getenv("SILICONFLOW_MODEL", "Qwen/Qwen2.5-32B-Instruct"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7"))
        )
    
    def _create_llm(self, config: LLMConfig) -> ChatOpenAI:
        """
        Create ChatOpenAI instance from configuration.
        
        Args:
            config: LLM configuration
            
        Returns:
            Configured ChatOpenAI instance
        """
        return ChatOpenAI(
            model=config.model,
            api_key=config.api_key,
            base_url=config.base_url,
            temperature=config.temperature
        )
    
    def _log_configuration(self) -> None:
        """Log LLM configuration details."""
        self.logger.info("LLM Configuration:")
        self.logger.info(f"  Primary API Key: {self.primary_config.api_key[:20] if self.primary_config.api_key else 'None'}...")
        self.logger.info(f"  Primary Base URL: {self.primary_config.base_url}")
        self.logger.info(f"  Primary Model: {self.primary_config.model}")
        self.logger.info(f"  Primary Temperature: {self.primary_config.temperature}")
        self.logger.info(f"  Fallback API Key: {self.fallback_config.api_key[:20] if self.fallback_config.api_key else 'None'}...")
        self.logger.info(f"  Fallback Base URL: {self.fallback_config.base_url}")
        self.logger.info(f"  Fallback Model: {self.fallback_config.model}")
    
    def _should_fallback(self, error: Exception) -> bool:
        """
        Determine if an error warrants falling back to secondary LLM.
        
        Args:
            error: The exception that occurred
            
        Returns:
            True if should fallback, False otherwise
        """
        error_str = str(error).lower()
        return (
            "429" in str(error) or 
            "quota" in error_str or 
            "rate" in error_str or
            "500" in str(error) or
            "internal server error" in error_str or
            "internalservererror" in type(error).__name__.lower() or
            "server error" in error_str
        )
    
    async def invoke(self, messages: List[BaseMessage]) -> str:
        """
        Invoke LLM with automatic fallback strategy.
        
        Args:
            messages: List of messages to send to LLM
            
        Returns:
            LLM response content
            
        Raises:
            Exception: If both primary and fallback LLMs fail
        """
        self.logger.info("=== Starting LLM invocation ===")
        self.logger.info(f"Message count: {len(messages)}")
        
        # Try primary LLM first
        try:
            self.logger.info("Attempting primary LLM invocation...")
            response = await self.primary_llm.ainvoke(messages)
            self.logger.info("=== Primary LLM invocation successful ===")
            self.logger.info(f"Primary API: {getattr(self.primary_llm, 'openai_api_base', 'default')}")
            self.logger.info(f"Primary Model: {getattr(self.primary_llm, 'model_name', self.primary_config.model)}")
            self.logger.info(f"Response length: {len(response.content)}")
            self.logger.info(f"Response preview: {response.content[:200]}...")
            return response.content
            
        except Exception as primary_error:
            self.logger.warning("=== Primary LLM invocation failed ===")
            self.logger.warning(f"Primary error type: {type(primary_error).__name__}")
            self.logger.warning(f"Primary error message: {str(primary_error)}")
            
            # Check if should fallback
            if self._should_fallback(primary_error):
                self.logger.info(f"Detected fallback-eligible error: {type(primary_error).__name__}")
                
                try:
                    self.logger.info("Attempting fallback LLM invocation...")
                    fallback_response = await self.fallback_llm.ainvoke(messages)
                    self.logger.info("=== Fallback LLM invocation successful ===")
                    self.logger.info(f"Fallback API: {self.fallback_config.base_url}")
                    self.logger.info(f"Fallback Model: {self.fallback_config.model}")
                    self.logger.info(f"Fallback response length: {len(fallback_response.content)}")
                    self.logger.info(f"Fallback response preview: {fallback_response.content[:200]}...")
                    return fallback_response.content
                    
                except Exception as fallback_error:
                    self.logger.error("=== Fallback LLM invocation also failed ===")
                    self.logger.error(f"Fallback error type: {type(fallback_error).__name__}")
                    self.logger.error(f"Fallback error message: {str(fallback_error)}")
                    # If fallback also fails, raise original error
                    raise primary_error
            else:
                # If not fallback-eligible, raise original error
                self.logger.error("=== Non-fallback-eligible error, not using fallback strategy ===")
                self.logger.error(f"Error type: {type(primary_error).__name__}")
                self.logger.error(f"Error details: {str(primary_error)}")
                raise primary_error
    
    def get_primary_model_info(self) -> dict:
        """
        Get information about the primary LLM.
        
        Returns:
            Dictionary with primary model information
        """
        return {
            "model": self.primary_config.model,
            "base_url": self.primary_config.base_url,
            "temperature": self.primary_config.temperature,
            "has_api_key": bool(self.primary_config.api_key)
        }
    
    def get_fallback_model_info(self) -> dict:
        """
        Get information about the fallback LLM.
        
        Returns:
            Dictionary with fallback model information
        """
        return {
            "model": self.fallback_config.model,
            "base_url": self.fallback_config.base_url,
            "temperature": self.fallback_config.temperature,
            "has_api_key": bool(self.fallback_config.api_key)
        }