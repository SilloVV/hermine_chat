from typing import Optional, Generator,Tuple, List, Any

# Pour charger les variables d'environnement
from .env_variable_loader import load_var_env

# Mistral AI
from mistralai import Mistral
from langchain_mistralai import ChatMistralAI


#Variables utiles
API_KEY_NAME=load_var_env("API_KEY_NAME")
MODEL_NAME= load_var_env("MODEL_NAME") 

def try_api_key(API_KEY: str) -> bool: ## <--- à voir si c'est vraiment utile : augmente le request rate initialement RPS -> https://docs.mistral.ai/deployment/laplateforme/tier/
    """
    teste si la clé API est correcte avec un appel LLM à 1 token de sortie et 3 tokens d'entrée
    """
    try:
        client = Mistral(api_key=API_KEY)
        chat_response = client.chat.complete(
         model = "mistral-large-latest",
        messages = [
				{
					"role": "user",
					"content": "",
				},
			],
			max_tokens=1,
		)
        # print(f"Réponse de l'API: {chat_response}")
        return True
    except Exception as e:
        print(f"Erreur: {e}")
        return False
    

def initialize_llm(model: str, max_output_tokens: int, temperature: float = 0.1) -> None:
    """
    initlialise le modèle LLM : une requète à 1 token de sortie et 3 tokens d'entrée est faite à chaque appel de cette fonction
	pour vérifier si la clé API est valide.
    """
    
    if not try_api_key(load_var_env(API_KEY_NAME)):
        raise ValueError(f"API key {API_KEY_NAME} is not valid.")
    
    # La doc ChatMistralAI est dispo ici : https://docs.mistral.ai/api/#tag/chat/operation/chat_completion_v1_chat_completions_post
    llm = ChatMistralAI(
            model=model,
            temperature=temperature,
            max_tokens=max_output_tokens,
     )
    return llm


def stream_chat_response(llm, messages):
    """Générateur qui produit les morceaux de réponse un par un."""
    try:
        for chunk in llm.stream(messages):
            yield chunk.content
    except Exception as e:
        yield f"[Erreur de communication: {e}]"

# Utilisation dans une interface de chat
def display_streaming_response(llm, messages):
    print("\nAssistant: ", end="", flush=True)
    full_response = ""
    
    for text_chunk in stream_chat_response(llm, messages):
        print(text_chunk, end="", flush=True)
        full_response += text_chunk
        time.sleep(0.01)  # Optionnel: simule un délai de frappe naturel
    
    print("\n")
    return full_response 
