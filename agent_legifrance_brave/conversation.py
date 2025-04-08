from LLM.init_llm import initialize_llm
from LLM.env_variable_loader import load_var_env
from agent_legifrance_brave.utils_conversation import parse_json_model_output, format_response , detect_search_request
from agent_legifrance_brave.tools.appel_api import api_call
from langchain_community.tools import BraveSearch
import json
import time


# Pour charger les variables d'environnement
MODEL_NAME=load_var_env("MODEL_NAME")
MEMORY_WINDOW = 5 # nombre de messages à garder dans la mémoire de la conversation
SEARCH_API_KEY_NAME = load_var_env("SEARCH_API_KEY_NAME")
SEARCH_API_KEY_VALUE = load_var_env(SEARCH_API_KEY_NAME)
NUMBER_OF_RESULTS = 5  # nombre de résultats à retourner

# prompt de système
from .prompting.prompts import system_prompt
from .utils_conversation import (
    ask_user_input,
    display_streaming_response,
    keep_window_buffer,
    display_context,
    count_interactions,
)

def main():
    """
    Fonction principale de la conversation
    """
    # Initialiser le modèle LLM principal
    llm = initialize_llm(MODEL_NAME, temperature=0.3, max_output_tokens=1000) 
    
    # Initialiser un second LLM spécifique pour la synthèse, avec un system prompt différent
    synthesis_system_prompt = """Tu es un assistant juridique spécialisé dans la synthèse d'informations pour répondre à une question utilisateur.
    Tu peux faire plusieurs recherches internet (entre 3 et 10) pour approfondir ton analyse. Pour chaque recherche, écris sur une ligne SEARCH: <la recherche que tu souhaites faire>.
    Ta tâche est de combiner les informations juridiques de l'api Legifrance avec des données complémentaires trouvées sur internet et UNIQUEMENT selon ces informations.
    Tu dois produire des synthèses claires et informatives en français standard, JAMAIS en format JSON.
    Tu présentes les points clés des textes juridiques et expliques comment les informations externes les complètent ou les contextualisent.
    Assure-toi de faire plusieurs recherches variées pour couvrir différents aspects du sujet juridique."""
    
    synthesis_llm = initialize_llm(MODEL_NAME, temperature=0.1, max_output_tokens=1000)
    
    # Initialiser l'outil de recherche BraveSearch
    search_tool = BraveSearch.from_api_key(
        api_key=SEARCH_API_KEY_VALUE, 
        search_kwargs={"count": NUMBER_OF_RESULTS}
    )
    
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
            user_input = ask_user_input()
            if user_input.lower() == 'exit':
                break
            
            # Ajouter le message de l'utilisateur
            messages.append(("human", user_input))
            
            # Obtenir la réponse
            print(f"Réponse du LLM :")
            full_response = display_streaming_response(llm, messages)
            
            # Ajouter la réponse au contexte pour la prochaine itération
            messages.append(("assistant", full_response))
            
            # Vérifier s'il y a des demandes de recherche internet explicites
            search_queries = detect_search_request(full_response)
            if search_queries:
                for i, query in enumerate(search_queries, 1):
                    print(f"\nRecherche {i}/{len(search_queries)} en cours pour: {query}...")
                    search_results = search_tool.invoke(query)
                    formatted_results = format_response(search_results)
                    
                    # Ajouter les résultats au contexte
                    search_results_message = f"Résultats de la recherche internet {i} pour '{query}':\n{formatted_results}"
                    messages.append(("assistant", search_results_message))
                    print(f"INFO: Résultats de la recherche {i} ajoutés au contexte")
                
                # Informer l'utilisateur
                print(f"\n{len(search_queries)} recherches internet effectuées et résultats ajoutés au contexte.")
                        
            # Parser la réponse JSON pour Legifrance
            cleaned_json_str = parse_json_model_output(full_response)
            
            #Appel API
            try:
                # Tenter de convertir la chaîne en objet JSON
                payload = json.loads(cleaned_json_str)
                
                # Si un payload valide est détecté, appeler l'API Legifrance
                if payload:
                    print("\nINFO: Appel de l'API Legifrance avec le payload généré...")
                    api_results = api_call(payload)
                    
                    # Afficher les résultats de l'appel API
                    print("\nINFO: Résultats de l'API Legifrance :")
                    print(api_results)
                    if (api_results is None) or (api_results == ([],[])):
                        print("Aucun résultat trouvé.\n")
                        print("relançons la recherche avec un autre payload...")
                        messages.append(("assistant", "Aucun résultat trouvé. Relançons la recherche avec un autre payload."))
                        # Relancer le LLM avec un nouveau contexte
                        retry_context = [
                            ("system", system_prompt),
                            ("human", user_input),
                            ("assistant", "Aucun résultat trouvé. Relançons la recherche avec un autre payload.")
                        ]
                        retry_response = display_streaming_response(llm, retry_context)
                        messages.append(("assistant", retry_response))
                    
                    # Traiter les résultats de l'API Legifrance
                    if isinstance(api_results, tuple) and len(api_results) >= 2:
                        titres, cids = api_results
                        for i, (titre, cid) in enumerate(zip(titres, cids), 1):
                            print("résultats debugs:")
                            print(f"{i}. {titre} - CID: {cid}")
                        
                        # Ajouter les résultats au contexte pour que le LLM puisse y accéder
                        results_message = f"Résultats de l'API Legifrance : {list(zip(titres, cids))}"
                        messages.append(("assistant", results_message))
                        
                        # SYNTHÈSE AVEC RECHERCHES MULTIPLES
                        if titres:
                            # Initialiser le contexte de synthèse
                            synthesis_context = [
                                ("system", synthesis_system_prompt),
                                ("human", user_input),
                                ("assistant", f"J'ai trouvé les informations juridiques suivantes sur Legifrance concernant: {titres[0]}"),
                                ("assistant", results_message),
                                ("human", "Basé sur ces informations juridiques, fais plusieurs recherches internet (3 à 10) pour approfondir le sujet et me faire une synthèse complète.")
                            ]
                            
                            # Première phase: demander au LLM les recherches à effectuer
                            print("Planification des recherches internet complémentaires...")
                            search_plan_response = display_streaming_response(synthesis_llm, synthesis_context)
                            
                            # Extraire les requêtes de recherche
                            search_requests = detect_search_request(search_plan_response)
                            
                            # Limiter le nombre de recherches entre 3 et 10
                            search_requests = search_requests[:min(10, max(3, len(search_requests)))]
                            
                            print(f"INFO: {len(search_requests)} recherches internet planifiées.")
                            
                            # Exécuter chaque recherche et ajouter les résultats au contexte
                            for i, query in enumerate(search_requests, 1):
                                print(f"\nRecherche {i}/{len(search_requests)}: {query}")
                                
                                search_results = search_tool.invoke(query)
                                time.sleep(3)  # Pause pour éviter de surcharger l'API
                                formatted_results = format_response(search_results)
                                
                                search_results_message = f"Résultats de la recherche {i} pour '{query}':\n{formatted_results}"
                                synthesis_context.append(("assistant", search_results_message))
                                
                                print(f"INFO: Résultats de la recherche {i} ajoutés au contexte")
                            
                            # Demander la synthèse finale
                            synthesis_context.append(("human", "Maintenant que tu as toutes ces informations, peux-tu me faire une synthèse claire et complète qui combine les informations juridiques et les données complémentaires?"))
                            
                            # Obtenir la synthèse du second LLM
                            print(f"Génération de la synthèse finale...")
                            synthesis_response = display_streaming_response(synthesis_llm, synthesis_context)
                            
                            # Ajouter la synthèse au contexte principal
                            messages.append(("assistant", synthesis_response))
                    else:
                        print(api_results)  # Cas d'erreur ou autre format de retour
                        # Ajouter les résultats au contexte
                        results_message = f"Résultats de l'API Legifrance : {api_results}"
                        messages.append(("assistant", results_message))
                        
            except json.JSONDecodeError:
                print("INFO: Le LLM n'a pas généré de JSON valide pour l'appel à l'API.")
            except Exception as e:
                print(f"Erreur lors de l'appel à l'API : {str(e)}")
            
            # Garder la fenêtre de mémoire
            messages = keep_window_buffer(messages, MEMORY_WINDOW)
            
        except KeyboardInterrupt:
            print("\nInterruption de l'utilisateur.")
            break
                
if __name__ == "__main__":
    main()


