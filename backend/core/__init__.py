"""
Core module for configuration, logging, and middleware setup.
"""
from .config import settings
from .logging_config import configure_logging, get_logger
from .middleware import setup_middleware

__all__ = ["settings", "configure_logging", "get_logger", "setup_middleware"]