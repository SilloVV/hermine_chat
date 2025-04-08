from LLM.init_llm import initialize_llm
from LLM.env_variable_loader import load_var_env
from agent_payload_legifrance.utils_conversation import parse_json_model_output
from agent_payload_legifrance.tools.appel_api import api_call
import json



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
            
            # Obtenir la réponse
            print(f"Réponse du LLM :")
            full_response = display_streaming_response(llm, messages)
            
            # Ajouter la réponse au contexte pour la prochaine itération
            messages.append(("assistant", full_response))
            
            # Parser la réponse JSON
            cleaned_json_str = parse_json_model_output(full_response)
            
            try:
                # Tenter de convertir la chaîne en objet JSON
                payload = json.loads(cleaned_json_str)
                
                # Si un payload valide est détecté, appeler l'API Legifrance
                if payload:
                    print("\nAppel de l'API Legifrance avec le payload généré...")
                    api_results = api_call(payload)
                    
                    # Afficher les résultats de l'appel API
                    print("\nRésultats de l'API Legifrance :")
                    if (api_results is None) or (api_results == []):
                        print("Aucun résultat trouvé.\n")
                        print("relançons la recherche avec un autre payload...")
                        messages.append(("assistant", "Aucun résultat trouvé. Relançons la recherche avec un autre payload."))
                        continue
                    if isinstance(api_results, tuple) and len(api_results) == 2:
                        titres, cids = api_results
                        for i, (titre, cid) in enumerate(zip(titres, cids), 1):
                            print(f"{i}. {titre} - CID: {cid}")
                    else:
                        print(api_results)  # Cas d'erreur ou autre format de retour
                    
                    # Ajouter les résultats au contexte pour que le LLM puisse y accéder
                    results_message = f"Résultats de l'API Legifrance : {api_results}"
                    messages.append(("assistant", results_message))
            except json.JSONDecodeError:
                print("Le LLM n'a pas généré de JSON valide pour l'appel à l'API.")
            except Exception as e:
                print(f"Erreur lors de l'appel à l'API : {str(e)}")
            
            # Garder la fenêtre de mémoire
            messages = keep_window_buffer(messages, MEMORY_WINDOW)
            
        except KeyboardInterrupt:
            print("\nInterruption de l'utilisateur.")
            break


if __name__ == "__main__":
    main()


