import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm
from rich.console import Console
from rich.table import Table

# Load environment variables
load_dotenv()

def load_json_data(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_models_list(file_path):
    """Load models list, filtering out commented lines."""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.read().strip().split('\n')
    
    # Keep all models but mark which are active
    models = []
    for line in lines:
        line = line.strip()
        if line:
            if line.startswith('#'):
                # Keep commented models but mark them as inactive
                models.append({'name': line[1:], 'active': False})
            else:
                models.append({'name': line, 'active': True})
    
    return models

def setup_openai_client(base_url=None):
    """Setup OpenAI client for either Ollama or OpenAI API."""
    if base_url:
        # For Ollama
        return OpenAI(base_url=base_url, api_key="ollama")
    else:
        # For OpenAI API
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_completion(client, model, prompt):
    """Generate completion using the specified model."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def create_output_structure(prompt_type, model_name):
    """Create output directory structure for a model and prompt type."""
    output_dir = Path("output") / prompt_type / model_name
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def save_word_result(output_dir, word_data, prompt, response, prompt_type):
    """Save individual word result to JSON file."""
    result = {
        "word": word_data["word"],
        "actual_definition": word_data["answer"],
        "prompt": prompt,
        "model_response": response,
        "judge_result": "",
        "judge_reasoning": ""
    }
    
    file_path = output_dir / f"{word_data['word']}.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

def process_models_with_ollama(vocabulary, models, prompt_a_template, prompt_b_template):
    """Process all active models using Ollama."""
    ollama_client = setup_openai_client("http://localhost:11434/v1")
    
    for model in models:
        if not model['active']:
            print(f"Skipping commented model: {model['name']}")
            continue
            
        model_name = model['name']
        print(f"\nProcessing model: {model_name}")
        
        # Create separate output directories for prompt A and prompt B
        output_dir_a = create_output_structure("prompt_a", model_name)
        output_dir_b = create_output_structure("prompt_b", model_name)
        
        # Process each word with progress bar
        for word_data in tqdm(vocabulary, desc=f"Processing {model_name}"):
            # Process prompt A
            prompt_a = prompt_a_template.format(word=word_data["word"])
            response_a = generate_completion(ollama_client, model_name, prompt_a)
            save_word_result(output_dir_a, word_data, prompt_a, response_a, "prompt_a")
            
            # Process prompt B
            prompt_b = prompt_b_template.format(word=word_data["word"])
            response_b = generate_completion(ollama_client, model_name, prompt_b)
            save_word_result(output_dir_b, word_data, prompt_b, response_b, "prompt_b")

def judge_responses():
    """Use GPT-4 to judge all model responses."""
    openai_client = setup_openai_client()
    output_path = Path("output")
    
    if not output_path.exists():
        print("No output directory found. Run model processing first.")
        return
    
    print("\nJudging responses with GPT-4...")
    
    # Process prompt_a and prompt_b directories separately
    for prompt_type in ["prompt_a", "prompt_b"]:
        prompt_dir = output_path / prompt_type
        if not prompt_dir.exists():
            print(f"No {prompt_type} directory found.")
            continue
        
        print(f"\nJudging {prompt_type} responses...")
        
        for model_dir in prompt_dir.iterdir():
            if not model_dir.is_dir():
                continue
                
            print(f"Judging responses for model: {model_dir.name}")
            
            word_files = list(model_dir.glob("*.json"))
            for word_file in tqdm(word_files, desc=f"Judging {model_dir.name}"):
                with open(word_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Skip if already judged
                if data.get("judge_result"):
                    continue
                
                if prompt_type == "prompt_a":
                    # Judge prompt A response
                    judge_prompt = f"""
                    Compare the following two definitions of the Spanish word "{data['word']}":

                    Actual definition: {data['actual_definition']}
                    Model response: {data['model_response']}

                    Is the model's response substantially correct? It doesn't need to be word-for-word identical, but should capture the main meaning and be reasonably accurate.

                    Respond with either "correct" or "incorrect", followed by a brief explanation of your reasoning.
                    """
                else:
                    # Judge prompt B response
                    judge_prompt = f"""
                    Evaluate the following response to a Spanish word exercise for the word "{data['word']}":

                    Task: Write two sentences - one using the word '{data['word']}', and another related sentence that doesn't contain the word but complements its meaning.
                    
                    Model response: {data['model_response']}

                    Does the model's response fulfill the task correctly? It should contain two sentences: one with the target word and one related sentence without it.

                    Respond with either "correct" or "incorrect", followed by a brief explanation of your reasoning.
                    """
                
                judge_response = generate_completion(openai_client, "gpt-4", judge_prompt)
                
                # Parse judge response
                if judge_response.lower().startswith("correct"):
                    data["judge_result"] = "correct"
                else:
                    data["judge_result"] = "incorrect"
                
                data["judge_reasoning"] = judge_response
                
                # Save updated result
                with open(word_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

def create_summary():
    """Create summary.json with all results."""
    output_path = Path("output")
    summary = {}
    
    if not output_path.exists():
        print("No output directory found.")
        return summary
    
    # Collect models from both prompt directories
    all_models = set()
    prompt_a_dir = output_path / "prompt_a"
    prompt_b_dir = output_path / "prompt_b"
    
    if prompt_a_dir.exists():
        all_models.update([d.name for d in prompt_a_dir.iterdir() if d.is_dir()])
    if prompt_b_dir.exists():
        all_models.update([d.name for d in prompt_b_dir.iterdir() if d.is_dir()])
    
    for model_name in all_models:
        correct_count_a = 0
        total_count_a = 0
        correct_count_b = 0
        total_count_b = 0
        
        # Count prompt A results
        model_dir_a = prompt_a_dir / model_name
        if model_dir_a.exists():
            for word_file in model_dir_a.glob("*.json"):
                with open(word_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if data.get("model_response"):
                    total_count_a += 1
                    if data.get("judge_result") == "correct":
                        correct_count_a += 1
        
        # Count prompt B results
        model_dir_b = prompt_b_dir / model_name
        if model_dir_b.exists():
            for word_file in model_dir_b.glob("*.json"):
                with open(word_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if data.get("model_response"):
                    total_count_b += 1
                    if data.get("judge_result") == "correct":
                        correct_count_b += 1
        
        summary[model_name] = {
            "prompt_a_correct": correct_count_a,
            "prompt_a_total": total_count_a,
            "prompt_b_correct": correct_count_b,
            "prompt_b_total": total_count_b
        }
    
    # Save summary
    with open("summary.json", 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    return summary

def print_results_table(summary):
    """Print results table using rich."""
    console = Console()
    table = Table(title="Model Performance Summary")
    
    table.add_column("Model", style="cyan", no_wrap=True)
    table.add_column("Prompt A Correct", style="green")
    table.add_column("Prompt B Correct", style="yellow")
    
    for model_name, results in summary.items():
        prompt_a_results = f"{results['prompt_a_correct']}/{results['prompt_a_total']}"
        prompt_b_results = f"{results['prompt_b_correct']}/{results['prompt_b_total']}"
        
        table.add_row(model_name, prompt_a_results, prompt_b_results)
    
    console.print(table)

def main():
    """Main execution function."""
    print("Loading data files...")
    
    # Load vocabulary and prompts
    vocabulary = load_json_data("suite/vocabulary_short.json")
    models = load_models_list("suite/models_list.txt")
    prompts = load_json_data("suite/prompts.json")
    
    # Get both prompts
    prompt_a = prompts["prompt_a"]
    prompt_b = prompts["prompt_b"]
    
    print(f"Loaded {len(vocabulary)} words")
    print(f"Loaded {len([m for m in models if m['active']])} active models")
    print(f"Using prompt A: {prompt_a}")
    print(f"Using prompt B: {prompt_b}")
    
    # Step 1: Process all models with Ollama
    print("\n=== Processing models with Ollama ===")
    process_models_with_ollama(vocabulary, models, prompt_a, prompt_b)
    
    # Step 2: Judge responses with GPT-4
    print("\n=== Judging responses ===")
    judge_responses()
    
    # Step 3: Create summary and display results
    print("\n=== Creating summary ===")
    summary = create_summary()
    
    print("\n=== Results ===")
    print_results_table(summary)
    
    print("\nSummary saved to summary.json")
    print("Experiment completed successfully!")

if __name__ == "__main__":
    main()