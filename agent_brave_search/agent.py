
# init LLM 
from LLM.init_llm import initialize_llm

MODEL_NAME="mistral-large-latest" # voir : https://docs.mistral.ai/getting-started/models/models_overview/ pour d'autres modèles
llm = initialize_llm(MODEL_NAME, temperature=0.1, max_output_tokens=1000) 

# import des prompts 
from prompting.prompts import system_prompt

# import des outils 
# définition de l'agent 
