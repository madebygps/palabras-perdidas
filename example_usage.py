"""Example usage of the modular components."""

from pathlib import Path
from src.config import Config
from src.vocabulary import VocabularyManager
from src.prompts import PromptManager
from src.models import ModelManager


def example_vocabulary_usage():
    """Demonstrate vocabulary module usage."""
    print("=== Vocabulary Module Example ===")
    config = Config(Path(__file__).parent)
    vocab_manager = VocabularyManager(config)
    
    # Load vocabulary
    vocab_manager.load_vocabulary("vocabulary_short.json")
    
    # Access words
    for i in range(min(3, vocab_manager.get_word_count())):
        word = vocab_manager.get_word_by_index(i)
        if word:
            print(f"{i+1}. {word.word}: {word.answer[:50]}...")
    print()


def example_prompt_usage():
    """Demonstrate prompt module usage."""
    print("=== Prompt Module Example ===")
    config = Config(Path(__file__).parent)
    prompt_manager = PromptManager(config)
    
    # Load prompts
    prompt_manager.load_prompts("prompts.json")
    
    # Use prompts with different words
    test_words = ["casa", "perro", "libro"]
    for word in test_words:
        prompt = prompt_manager.get_prompt("prompt_a", word=word)
        print(f"Prompt for '{word}': {prompt}")
    print()


def example_model_usage():
    """Demonstrate model module usage."""
    print("=== Model Module Example ===")
    config = Config(Path(__file__).parent)
    model_manager = ModelManager(config)
    
    # Load models
    model_manager.load_models("models_list.txt")
    
    # Display available models
    print(f"Found {model_manager.get_model_count()} available models:")
    for model in model_manager.get_models():
        print(f"  - {model}")
    print()


if __name__ == "__main__":
    example_vocabulary_usage()
    example_prompt_usage()
    example_model_usage()
