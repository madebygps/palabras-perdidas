"""Vocabulary data management."""

from dataclasses import dataclass
from typing import List
from .config import Config


@dataclass
class Word:
    """Represents a vocabulary word with its answer."""
    word: str
    answer: str


class VocabularyManager:
    """Manages vocabulary word lists."""

    def __init__(self, config: Config):
        """Initialize vocabulary manager.
        
        Args:
            config: Configuration instance for loading files.
        """
        self.config = config
        self._words: List[Word] = []

    def load_vocabulary(self, filename: str = "vocabulary_short.json") -> None:
        """Load vocabulary from a JSON file.
        
        Args:
            filename: Name of vocabulary file to load.
        """
        data = self.config.load_json(filename)
        self._words = [Word(**item) for item in data]

    def get_words(self) -> List[Word]:
        """Get all loaded vocabulary words.
        
        Returns:
            List of Word objects.
        """
        return self._words

    def get_word_by_index(self, index: int) -> Word | None:
        """Get a specific word by index.
        
        Args:
            index: Index of the word to retrieve.
            
        Returns:
            Word object or None if index is out of range.
        """
        if 0 <= index < len(self._words):
            return self._words[index]
        return None

    def get_word_count(self) -> int:
        """Get the number of loaded words.
        
        Returns:
            Count of vocabulary words.
        """
        return len(self._words)
