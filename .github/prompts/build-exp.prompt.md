---
mode: agent
---

# Spanish Word Understanding Test Script

Build a script to test locally running LLM models for their understanding of Spanish words.

## Step-by-Step Implementation Guide

### 1. Environment & Constraints
1. Use existing virtual environment: `/Users/gps/Developer/palabras-perdidas/.venv/bin/activate` (only source if not already active).
2. Only add dependencies with: `uv add <package>`.
3. Run the experiment only with: `uv run main.py`.
4. All logic must live inside `main.py` (no other Python files created).

### 2. Load Inputs
1. Read `suite/vocabulary_short.json` → list of objects with fields: `word`, `answer` (reference definition; not sent to model).
2. Read `suite/models_list.txt` → one model per line.
3. Filter models: skip lines that (after stripping leading/trailing whitespace) start with `#` or are empty.
4. Active model names are the raw (uncommented) line contents (preserve colons, versions, etc.).
5. Read `suite/prompts.json` and extract key `prompt_a` (string containing `{word}` placeholder).

### 3. Prompt Preparation
1. Base template: value of `prompt_a` (currently: `Dime la definición de la palabra '{word}'.`).
2. For each vocabulary entry, produce final prompt by replacing `{word}` with the exact word string.
3. (Do not leak the reference definition to the model.)

### 4. Model Client Setup
1. Use the OpenAI Python package to call locally hosted Llama-compatible models (assumption: they are exposed via an OpenAI-compatible endpoint on localhost). Environment configuration: store any required secrets/vars (e.g., `OPENAI_BASE_URL`, `OPENAI_API_KEY`, custom base URL) in a root `.env` file; load them in `main.py` (e.g., via `python-dotenv`) and NEVER hardcode secrets.
2. Instantiate a client once (reuse across calls). If a custom base URL is required, allow configuration via environment variable (e.g., `LOCAL_OPENAI_BASE_URL`).
3. For each model name, call the chat/completions (or completions) endpoint with the constructed prompt.
4. Use a short, conservative temperature (e.g., 0.2) unless overridden by env var.
5. Implement simple retry (e.g., up to 3 attempts with exponential backoff on transient errors / connection issues).

### 5. Directory & Output Layout
1. Ensure an `output/` directory exists at repo root.
2. For each active model create `output/{model_name}/` (sanitize path if needed—retain colons if filesystem allows; on macOS it's fine).
3. For each word, create a JSON file: `output/{model_name}/{word}.json`.
4. JSON file structure (example):
	 ```json
	 {
		 "model": "mixtral:latest",
		 "word": "ardilla",
		 "prompt": "Dime la definición de la palabra 'ardilla'.",
		 "response": "<model raw text>",
		 "reference_definition": "Mamífero roedor...", 
		 "timestamp": "2025-10-02T12:34:56Z"
	 }
	 ```
5. Overwrite existing file if re-running (or optionally skip if exists—decide via a constant/flag; default: overwrite for reproducibility).



### 6. Execution & Judging Workflow
Two phases: (A) Definition Generation (local models) with progress bar, (B) Judging (GPT‑5) with separate progress bar, then summary table.

#### Phase A: Generate Definitions
1. Load data & prompts.
2. Derive active models list.
3. Initialize a Rich Progress (or similar) bar with total = (number_of_models × number_of_words).
4. For each model:
	 - Prepare model output directory.
	 - For each vocabulary entry:
		 - Build prompt (inject `{word}`).
		 - Query model with retry logic.
		 - Capture response text (strip).
		 - Write JSON record (see structure in Section 5).
		 - Advance progress bar (e.g., show "Model X: word Y (i/j)").
5. Close progress bar; optionally print a brief summary (counts of successes/failures per model).

#### Phase B: Judging with GPT‑5
1. Use OpenAI-hosted `gpt-5` (configurable via env var `JUDGE_MODEL`, default `gpt-5`). Requires standard OpenAI API key in `.env` (`OPENAI_API_KEY`).
2. Load all generated JSON files (or reuse in-memory cache if still present).
3. For each model/word pair, assemble judging prompt template (lenient criteria):
	 "Eres un evaluador. Palabra: '{word}'. Definición de referencia: '{reference_definition}'. Respuesta del modelo: '{model_response}'. ¿La respuesta captura correctamente la esencia del significado? Responde SOLO con 'correcto' o 'incorrecto' y nada más. Sé indulgente si el núcleo semántico es adecuado."
4. Call judge model; parse normalized output (lowercase, strip accents/spaces). Accept tokens starting with 'c' as correct, starting with 'i' as incorrect; else mark 'undetermined'.
5. Maintain per-model counters: `correct_count`, `total_words`.
6. Progress bar: total = number_of_models × number_of_words; show ticks like "Judging modelX (k/n)".
7. On judge API failure after retries, mark that word as incorrect (or store error) but continue.
8. Persist a summary artifact `output/summary.json` with structure:
	 ```json
	 {
		 "generated_at": "ISO8601",
		 "judge_model": "gpt-5",
		 "models": {
			 "mixtral:latest": {"correct": 7, "total": 10},
			 "gemma3:12b": {"correct": 6, "total": 10}
		 }
	 }
	 ```

#### Phase C: Summary Table (Rich)
1. After judging, render a Rich table with columns: `Model | % Correct (Prompt A) | % Correct (Prompt B)`.
2. Compute % as (correct / total * 100) rounded to 1 decimal.
3. Leave third column blank (placeholder for future Prompt B evaluation).
4. Example (ASCII approximation):
	 | Model           | % Correct (Prompt A) | % Correct (Prompt B) |
	 |-----------------|----------------------|----------------------|
	 | mixtral:latest  | 70.0                 |                      |
	 | gemma3:12b      | 60.0                 |                      |
	 | llama3.1:latest | 80.0                 |                      |

#### Dependencies to Add (via uv add)
- `rich` (tables + progress)
- Optionally `tqdm` (if preferred for generation; but Rich alone suffices)
- `python-dotenv` (if used for `.env` loading)

#### Environment Variables (.env)
- `OPENAI_API_KEY` (required for GPT‑5 judging)
- `OPENAI_BASE_URL` or custom local base (for local models)
- `JUDGE_MODEL` (optional override, default `gpt-5`)

Print concise per-item logs only if `VERBOSE=1`, otherwise rely on progress bars.

### 7. Error Handling & Resilience
1. If a model call fails after retries, write a JSON file with `response=null` and an `error` field capturing the exception message.
2. Continue processing remaining words and models even after failures.
3. Validate JSON structures before writing (ensure serializable types only).
4. If input files are missing or malformed, print an error and exit with non-zero status.

### 8. Logging / UX
1. Use simple `print()` statements—no external logging dependency unless already present.
2. Optional verbosity flag via environment variable `VERBOSE=1` to include full tracebacks on errors.

### 9. Assumptions (Documented)
1. Local models are exposed via an OpenAI-compatible API.
2. Colons in model names are acceptable as directory names on macOS.
3. `vocabulary_short.json` structure is stable (contains `word` and `answer`).

### 10. Completion Criteria
Success when: For every active (uncommented) model and every vocabulary word, a JSON file exists in its model directory containing either a model response or an error record.

## Final Expected Tree (Example)
```
output/
	mixtral:latest/
		ardilla.json
		corbata.json
		...
	gemma3:12b/
		ardilla.json
		...
	llama3.1:latest/
		ardilla.json
		...
```

## Next Step
Implement this logic inside `main.py` following the above contract.