from LLM.init_llm import initialize_llm
from LLM.env_variable_loader import load_var_env
from agent_payload_legifrance.utils_conversation import parse_json_model_output
from agent_payload_legifrance.tools import appel_api

# Pour charger les variables d'environnement
MODEL_NAME=load_var_env("MODEL_NAME")
MEMORY_WINDOW = 5 # nombre de messages à garder dans la mémoire de la conversation

# prompt de système
from .prompting.prompts import system_prompt
from .utils_conversation import (
    demander_entree_utilisateur,
    display_streaming_response,
    keep_window_buffer,
    display_context,
    count_interactions,
)


def main():
    """
    Fonction principale de la conversation
    """
    # Initialiser le modèle LLM
    llm = initialize_llm(MODEL_NAME, temperature=0.1, max_output_tokens=1000) 
    
    # Afficher le message de bienvenue
    print("Bienvenue dans la conversation avec le LLM !")
    print("Tapez 'exit' pour quitter.")
    
    messages = [
    (
        "system",
        system_prompt,
    ),
    ]  # Contexte initial de la conversation

    # Boucle principale de la conversation
    while True:
        try:
            user_input = demander_entree_utilisateur()
            if user_input.lower() == 'exit':
                break
            
            # Ajouter le message de l'utilisateur
            messages.append(("human", user_input))
            
            # Si l'utilisateur interrompt la conversation, on arrête le streaming
            
            # Obtenir la réponse
            print(f"Réponse du LLM :")
            full_response = display_streaming_response(llm, messages)
            # Ajouter la réponse au contexte pour la prochaine itération
            messages.append(("assistant", full_response))
            
            # Afficher le contexte actuel
            # display_context(messages)
            # print("Nombre d'intéractions : " + count_interactions(messages))
            
            # Garder la fenêtre de mémoire
            messages =  keep_window_buffer(messages, MEMORY_WINDOW)
            print(parse_json_model_output(full_response))
        except KeyboardInterrupt:
            print("\nInterruption de l'utilisateur.")
            break


if __name__ == "__main__":
    main()
