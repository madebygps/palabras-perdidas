"""Main entry point for Palabras Perdidas application."""

from pathlib import Path
from src.config import Config
from src.vocabulary import VocabularyManager
from src.prompts import PromptManager
from src.models import ModelManager
from src.llm_client import LLMClient


def main():
    """Main application entry point."""
    # Initialize configuration
    config = Config(Path(__file__).parent)
    
    # Initialize managers
    vocab_manager = VocabularyManager(config)
    prompt_manager = PromptManager(config)
    model_manager = ModelManager(config)
    llm_client = LLMClient()
    
    # Load data
    vocab_manager.load_vocabulary("vocabulary_short.json")
    prompt_manager.load_prompts("prompts.json")
    model_manager.load_models("models_list.txt")
    
    # Display loaded data
    print(f"Loaded {vocab_manager.get_word_count()} vocabulary words")
    print(f"Loaded {len(prompt_manager.get_all_prompts())} prompts")
    print(f"Loaded {model_manager.get_model_count()} models")
    
    # Example usage
    if vocab_manager.get_word_count() > 0:
        word = vocab_manager.get_word_by_index(0)
        if word:
            print(f"\nExample word: {word.word}")
            print(f"Answer: {word.answer}")
            
            # Example prompt formatting
            formatted_prompt = prompt_manager.get_prompt("prompt_a", word=word.word)
            print(f"\nFormatted prompt: {formatted_prompt}")
    
    # Display available models
    print(f"\nAvailable models:")
    for model in model_manager.get_models():
        print(f"  - {model}")


if __name__ == "__main__":
    main()
