---
mode: agent
---
# overview

We're gonna build an experiment that iterates over a list of words and prompts open weight models, the list of prompts based off the words. And our goal is to end up with a table of results on how well those models did with each prompt and each word. 

## task to achieve

Load all the words from the vocabulary_json file. Also load all the models from the models_list.txt file. But the ones that have a pound symbol at the beginning are commented out. I want them in the list, but we are not actively prompting them.

What we need to do is per each model, prompt, prompt a, from prompt prompts.json, create an output directory. And inside of that directory, a directory for every model. And inside of that directory, a word.json file for each of the words. In each JSON file, I'd like you to have the word, the correct definition, and the definition that the model provided.

Additionally, as the models are being prompted, let's have a progress bar in the terminal to show progress. 

## specific requirements

We are going to use the open AI package and olama locally for the model. Also make sure you are following the custom instructions I outlined in the python.instructions.md for running the code and for adding any dependencies. 


## constraints

All the code must stay inside of a single file main.py.

Do not create another file. 


