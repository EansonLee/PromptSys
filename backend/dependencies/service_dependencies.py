"""
Service dependency injection for FastAPI endpoints.
"""
from services.prompt_generator import PromptGenerator
from services.claude_cli_automation import claude_cli_automation
from services.gitlab_integration import gitlab_integration


def get_prompt_generator() -> PromptGenerator:
    """Dependency to get prompt generator service instance."""
    return PromptGenerator()


def get_claude_cli_service():
    """Dependency to get Claude CLI automation service instance."""
    return claude_cli_automation


def get_gitlab_service():
    """Dependency to get GitLab integration service instance."""
    return gitlab_integration