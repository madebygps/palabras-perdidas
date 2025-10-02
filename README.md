# Palabras Perdidas

A Spanish vocabulary learning application using Large Language Models (LLMs).

## Project Structure

```
palabras-perdidas/
├── main.py                 # Main entry point
├── src/                    # Source code modules
│   ├── __init__.py        # Package initialization
│   ├── config.py          # Configuration and file loading
│   ├── vocabulary.py      # Vocabulary data management
│   ├── prompts.py         # Prompt template management
│   ├── models.py          # Model list handling
│   └── llm_client.py      # LLM API client (placeholder)
└── suite/                  # Data files
    ├── vocabulary_short.json     # Short vocabulary list
    ├── vocabulary_complete.json  # Complete vocabulary list
    ├── prompts.json              # Prompt templates
    └── models_list.txt           # Available LLM models
```

## Modules

### config.py
Handles loading configuration and data files from the `suite/` directory.
- Load JSON files (vocabulary, prompts)
- Load text files (model lists)

### vocabulary.py
Manages vocabulary word lists with their definitions.
- Load vocabulary from JSON files
- Access words by index or iterate through all words
- Get word count

### prompts.py
Manages prompt templates for LLM interactions.
- Load prompt templates from JSON
- Format prompts with variable substitution (e.g., `{word}`)

### models.py
Manages the list of available LLM models.
- Load model list from text file
- Filter out commented lines (starting with `#`)
- Access available models

### llm_client.py
Placeholder for LLM API interactions.
- Interface for generating responses from LLMs
- Ready to implement with Ollama or other LLM APIs

## Usage

Run the main application:

```bash
python main.py
```

## Requirements

- Python >= 3.13

## Development

The codebase is now modular with clear separation of concerns:
- Each module has a single responsibility
- Easy to test individual components
- Simple to add new features or modify existing ones
- Well-documented with docstrings
