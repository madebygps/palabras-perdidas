# Palabras Perdidas

A comparative evaluation framework for testing Spanish language understanding across multiple LLMs using Ollama, with GPT-5 as the judge.

## Overview

This project evaluates how well different language models understand Spanish vocabulary by:
1. Generating responses using multiple Ollama models with two different prompts
2. Evaluating response accuracy using GPT-5 as a judge
3. Creating comparative performance reports

## Setup

### Prerequisites

- Python 3.13+
- [Ollama](https://ollama.ai/) installed and running locally
- OpenAI API key for GPT-5 judging

### Installation

1. Clone the repository:
```bash
git clone https://github.com/madebygps/palabras-perdidas.git
cd palabras-perdidas
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Create a `.env` file with your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

4. Configure models in `suite/models_list.txt` (comment out models with `#` to skip):
```
gemma3:12b
llama3.1:latest
# mixtral:latest
```

## Usage

Run the complete evaluation pipeline:

```bash
uv run main.py
```

This will:
1. Process all active models with both prompts against the vocabulary
2. Judge all responses using GPT-5
3. Generate a summary report and display results

### Prompts

- **Prompt A**: Definition request - "Dime la definición de la palabra '{word}'."
- **Prompt B**: Contextual usage - "Escribe dos frases, una con la palabra '{word}', y otra que no contenga esa palabra, pero que esté relacionada con la primera y complemente su significado."

### Vocabulary

Edit vocabulary files in the `suite/` directory:
- `vocabulary_short.json` - 10 words for quick testing
- `vocabulary_complete.json` - Full vocabulary set

## Output Structure

```
output/
├── prompt_a/
│   ├── gemma3:12b/
│   │   └── ardilla.json
│   └── llama3.1:latest/
│       └── ardilla.json
└── prompt_b/
    ├── gemma3:12b/
    │   └── ardilla.json
    └── llama3.1:latest/
        └── ardilla.json
summary.json
```

Each word file contains:
- Original word and definition
- Prompt used
- Model response
- Judge result (correct/incorrect)
- Judge reasoning

## Results

Results are displayed in a table showing correct/total for each model and prompt type:

```
Model Performance Summary
┌─────────────────┬─────────────────┬─────────────────┐
│ Model           │ Prompt A        │ Prompt B        │
│                 │ Correct         │ Correct         │
├─────────────────┼─────────────────┼─────────────────┤
│ gemma3:12b      │ 8/10            │ 10/10           │
│ llama3.1:latest │ 9/10            │ 7/10            │
└─────────────────┴─────────────────┴─────────────────┘
```

## License

MIT
