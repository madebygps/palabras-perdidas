import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm


def load_vocabulary(filepath: Path) -> list[dict[str, str]]:
    """Load vocabulary from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_models(filepath: Path) -> tuple[list[str], list[str]]:
    """Load models from text file, separating active and commented models."""
    active_models = []
    commented_models = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                commented_models.append(line[1:].strip())
            else:
                active_models.append(line)
    
    return active_models, commented_models


def load_prompts(filepath: Path) -> dict[str, str]:
    """Load prompts from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def query_model(client: OpenAI, model: str, prompt: str) -> str:
    """Query the model via Ollama and return the response."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        return f"Error: {str(e)}"


def save_result(output_dir: Path, prompt_name: str, model: str, word: str, correct_definition: str, model_definition: str, judgment: str | None = None, reasoning: str | None = None) -> None:
    """Save the result to a JSON file."""
    model_dir = output_dir / prompt_name / model
    model_dir.mkdir(parents=True, exist_ok=True)
    
    result = {
        "word": word,
        "correct_definition": correct_definition,
        "model_definition": model_definition
    }
    
    if judgment is not None:
        result["judgment"] = judgment
    if reasoning is not None:
        result["reasoning"] = reasoning
    
    output_file = model_dir / f"{word}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def judge_definition(judge_client: OpenAI, word: str, correct_definition: str, model_definition: str) -> tuple[str, str]:
    """Use GPT-4 to judge if the model's definition is correct."""
    judgment_prompt = f"""You are evaluating whether a model's definition of a Spanish word is correct.

Word: {word}
Correct Definition: {correct_definition}
Model's Definition: {model_definition}

The model's definition does not need to be word-for-word identical to the correct definition, but it must convey the same meaning. 

Respond with ONLY a JSON object in this exact format:
{{"judgment": "correct", "reasoning": "your explanation here"}}
or
{{"judgment": "incorrect", "reasoning": "your explanation here"}}

Do not include any other text before or after the JSON."""
    
    try:
        response = judge_client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are a precise evaluator that always responds with valid JSON only."},
                {"role": "user", "content": judgment_prompt}
            ]
        )
        
        result_text = response.choices[0].message.content or ""
        result_json = json.loads(result_text)
        return result_json.get("judgment", "error"), result_json.get("reasoning", "Failed to parse judgment")
    except Exception as e:
        return "error", f"Error during judgment: {str(e)}"


def print_results_table(results: dict[str, dict[str, int]]) -> None:
    """Print a formatted results table."""
    print("\n" + "="*70)
    print("EXPERIMENT RESULTS")
    print("="*70)
    print(f"{'Model':<25} {'Prompt A (Correct)':<25} {'Prompt B (Correct)':<20}")
    print("-"*70)
    
    for model, scores in results.items():
        prompt_a_score = scores.get("prompt_a", 0)
        prompt_b_score = "-"
        print(f"{model:<25} {prompt_a_score:<25} {prompt_b_score:<20}")
    
    print("="*70)


def main() -> None:
    """Main function to run the experiment."""
    load_dotenv()
    
    base_dir = Path(__file__).parent
    suite_dir = base_dir / "suite"
    output_dir = base_dir / "output"
    
    vocabulary = load_vocabulary(suite_dir / "vocabulary_short.json")
    active_models, commented_models = load_models(suite_dir / "models_list.txt")
    prompts = load_prompts(suite_dir / "prompts.json")
    
    prompt_name = "prompt_a"
    prompt_template = prompts[prompt_name]
    
    print(f"Loaded {len(vocabulary)} words")
    print(f"Active models: {len(active_models)}")
    print(f"Commented models: {len(commented_models)}")
    print(f"Using prompt: {prompt_name}")
    print(f"\nActive models: {', '.join(active_models)}")
    print(f"Commented models: {', '.join(commented_models)}")
    
    ollama_client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file")
    
    judge_client = OpenAI(api_key=openai_api_key)
    
    print("\n" + "="*70)
    print("PHASE 1: Generating Definitions")
    print("="*70)
    
    total_operations = len(active_models) * len(vocabulary)
    
    with tqdm(total=total_operations, desc="Generating") as pbar:
        for model in active_models:
            for word_entry in vocabulary:
                word = word_entry["word"]
                correct_definition = word_entry["answer"]
                
                prompt = prompt_template.format(word=word)
                model_definition = query_model(ollama_client, model, prompt)
                
                save_result(
                    output_dir=output_dir,
                    prompt_name=prompt_name,
                    model=model,
                    word=word,
                    correct_definition=correct_definition,
                    model_definition=model_definition
                )
                
                pbar.update(1)
    
    print(f"\n✓ Generation complete! Results saved to {output_dir}")
    
    print("\n" + "="*70)
    print("PHASE 2: Judging Definitions with GPT-4")
    print("="*70)
    
    results: dict[str, dict[str, int]] = {model: {"prompt_a": 0} for model in active_models}
    
    with tqdm(total=total_operations, desc="Judging") as pbar:
        for model in active_models:
            for word_entry in vocabulary:
                word = word_entry["word"]
                correct_definition = word_entry["answer"]
                
                word_file = output_dir / prompt_name / model / f"{word}.json"
                
                with open(word_file, 'r', encoding='utf-8') as f:
                    result_data = json.load(f)
                
                model_definition = result_data["model_definition"]
                
                judgment, reasoning = judge_definition(
                    judge_client, word, correct_definition, model_definition
                )
                
                save_result(
                    output_dir=output_dir,
                    prompt_name=prompt_name,
                    model=model,
                    word=word,
                    correct_definition=correct_definition,
                    model_definition=model_definition,
                    judgment=judgment,
                    reasoning=reasoning
                )
                
                if judgment == "correct":
                    results[model]["prompt_a"] += 1
                
                pbar.update(1)
    
    print(f"\n✓ Judging complete!")
    
    print_results_table(results)


if __name__ == "__main__":
    main()
