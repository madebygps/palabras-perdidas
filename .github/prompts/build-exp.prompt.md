---
mode: agent
---

# overview

I want to build an experiment with Python. We'll process words from a JSON file, prompt a list of models with a specific prompt, and obtain results showing how well each model performed on each prompt. The goal is to see how well these models understand Spanish words.

## specific requirements

- Use `uv add` to add any dependencies. 
- Use `uv remove` if you need to remove dependencies. 
- Use `uv run main.py` to run the code. 
- Do not use any other command to run any Python-specific functionality outside of these ones that I have outlined.
- Use the python-.env package to load our environment variables. I will have a .env file. You do not need to create one.

## constraints

- Keep all the code in a `main.py` file. Do not create another file.

## task list

1. Load all the files from the `suite/vocabulary_short.json`. These are all the words. Also load `models_list.txt`. In this file you’ll see a list of models we want to prompt. Some names start with a # symbol, which I use as a comment; keep them in the list but don’t use them actively. Also you have prompts.json; we’ll focus on just prompt A. Load all of these.

2. Now I need you to use the `OpenAI` package with the models loaded locally using `Olama` and execute the prompt against each model in that list. For each model, create an output directory; inside it, have a directory for the model, and within that a JSON file for each word (word.json). The JSON should contain the word, the actual definition, the prompt we asked, and the model’s response, plus an empty field for a judge to add later. While generating completions, use a progress‑bar package to show the progress of all words for each model.

3. Now I want you to use the `OpenAI` package and GPT-5 to judge each answer from all the models. Go through each model directory and each JSON file, and ask GPT-5 if the definition is correct. We care that it is relatively correct; it doesn't have to be word‑by‑word correct. Update the judge value in the word.json file to say “incorrect” or “correct,” and add a field for reasoning explaining why the judge decided that answer. I have a .env with the OpenAI API key already, so no need to create that.

4. After the judging is complete, I need you to create a `summary.json` with all of the results. Then I would also like you to use the rich package to print out a table to the terminal. Let's have three columns: the first one be the list of models, the second one be how many words were correct per prompt A, and the third one for the results of prompt B (keep it empty because we're not running it right now).


## success criteria

Success would be that we are able to ask all these models in the models underscore list.txt, prompt A, and then return a summary.json, and the table is printed out correctly in the terminal.