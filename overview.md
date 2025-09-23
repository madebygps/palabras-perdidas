
# Overview

I [read a paper](https://arxiv.org/abs/2403.15491) recently where the authors hypothesized that open-weight LLMs don’t understand most Spanish words. To test this, they randomly selected 100 words from Diccionario del Español Actual and queried 12 popular open conversational models (LLaMa, Mistral, Gemma, Yi, Bloomz, Flor, Bertin, etc.).

They designed a set of prompts in two categories: open-ended (to be evaluated manually) and binary yes/no (to be evaluated automatically, though less reliably). Here’s a summary of the prompts used:

| Category                                   | Label | Prompt (Spanish)                                                                                                                                                                                                                                                | Purpose                                                               | Evaluation Method                   |
| ------------------------------------------ | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ----------------------------------- |
| **Open-ended (Ground Truth)**              | **A** | *“Dime la definición de la palabra `<word>`.”* <br>(Give the definition of `<word>`.)                                                                                                                                                                           | Tests whether the model can **define the word correctly**.            | Manual check vs. dictionary.        |
|                                            | **B** | *“Escribe dos frases, una con la palabra `<word>`, y otra que no contenga esa palabra, pero que esté relacionada con la primera y complemente su significado.”* <br>(Write two sentences: one with `<word>`, another without it but related and complementary.) | Tests whether the model can **use the word meaningfully in context**. | Manual check by language expert.    |
| **Binary Yes/No (Automation Feasibility)** | **1** | *“¿Conoces el significado de la palabra `<word>`? Responde solo ‘Sí’ o ‘No’.”* <br>(Do you know the meaning of `<word>`? Yes/No only.)                                                                                                                          | Quick self-assessment of knowledge.                                   | Automatic scoring (but unreliable). |
|                                            | **2** | *“¿Existe la palabra `<word>` en castellano? Responde solo ‘Sí’ o ‘No’.”* <br>(Does `<word>` exist in Spanish? Yes/No only.)                                                                                                                                    | Tests recognition of word existence.                                  | Automatic scoring.                  |
|                                            | **3** | *“¿Es correcta la palabra `<word>` en castellano? Responde solo ‘Sí’ o ‘No’.”* <br>(Is `<word>` a valid word in Spanish? Yes/No only.)                                                                                                                          | Tests validity of the word.                                           | Automatic scoring.                  |


## Results

- Definitions: Fewer than half of the words were defined correctly by most models; the best only reached 66%.
- Usage in context: Almost all models failed here, with under 25% accuracy (many under 10%).
- Yes/No prompts: Unreliable and often misleading — some models just answered “No” to everything.
- Model size: Larger models like LLaMa-70B or Mixtral-46B did somewhat better, but still far from good.
- Spanish-optimized models (Bloomz, Flor, Bertin) surprisingly performed worse than general English/Chinese-focused ones.

Errors included English interference (“no se puede missed”), hybrid words (“ella es meana”), incorrect grammar, and inconsistent answers across prompts.

## Conclusion

In short, across the board, the models struggled, with less than 25% of words truly understood and used in context. The paper concludes that Spanish — and likely other underrepresented languages — is being left behind in the open-source LLM race, highlighting the need for more balanced multilingual training.