"""Configuration management for Palabras Perdidas."""

import json
from pathlib import Path
from typing import Any


class Config:
    """Handles loading and accessing configuration files."""

    def __init__(self, base_path: Path | None = None):
        """Initialize configuration with base path.
        
        Args:
            base_path: Base directory path. Defaults to project root.
        """
        if base_path is None:
            base_path = Path(__file__).parent.parent
        self.base_path = base_path
        self.suite_path = base_path / "suite"

    def load_json(self, filename: str) -> Any:
        """Load a JSON file from the suite directory.
        
        Args:
            filename: Name of the JSON file to load.
            
        Returns:
            Parsed JSON data.
        """
        file_path = self.suite_path / filename
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_text(self, filename: str) -> str:
        """Load a text file from the suite directory.
        
        Args:
            filename: Name of the text file to load.
            
        Returns:
            File contents as string.
        """
        file_path = self.suite_path / filename
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
