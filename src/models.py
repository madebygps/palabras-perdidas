"""Model list management."""

from typing import List
from .config import Config


class ModelManager:
    """Manages the list of available LLM models."""

    def __init__(self, config: Config):
        """Initialize model manager.
        
        Args:
            config: Configuration instance for loading files.
        """
        self.config = config
        self._models: List[str] = []

    def load_models(self, filename: str = "models_list.txt") -> None:
        """Load model list from a text file.
        
        Args:
            filename: Name of models file to load.
        """
        content = self.config.load_text(filename)
        self._models = [
            line.strip()
            for line in content.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]

    def get_models(self) -> List[str]:
        """Get all available model names.
        
        Returns:
            List of model names.
        """
        return self._models.copy()

    def get_model_count(self) -> int:
        """Get the number of available models.
        
        Returns:
            Count of models.
        """
        return len(self._models)
