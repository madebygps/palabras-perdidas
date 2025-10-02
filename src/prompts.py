"""Prompt template management."""

from typing import Dict
from .config import Config


class PromptManager:
    """Manages prompt templates for LLM interactions."""

    def __init__(self, config: Config):
        """Initialize prompt manager.
        
        Args:
            config: Configuration instance for loading files.
        """
        self.config = config
        self._prompts: Dict[str, str] = {}

    def load_prompts(self, filename: str = "prompts.json") -> None:
        """Load prompts from a JSON file.
        
        Args:
            filename: Name of prompts file to load.
        """
        self._prompts = self.config.load_json(filename)

    def get_prompt(self, prompt_key: str, **kwargs) -> str:
        """Get a formatted prompt by key.
        
        Args:
            prompt_key: Key of the prompt template.
            **kwargs: Variables to substitute in the template.
            
        Returns:
            Formatted prompt string.
        """
        template = self._prompts.get(prompt_key, "")
        return template.format(**kwargs)

    def get_all_prompts(self) -> Dict[str, str]:
        """Get all loaded prompts.
        
        Returns:
            Dictionary of prompt templates.
        """
        return self._prompts.copy()
