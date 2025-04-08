import time 
import re 

def display_context(messages):
    """
    Affiche le contexte actuel de la conversation
    """
    print("##################################")
    print("Contexte actuel :")
    for role, content in messages:
        print(f"{role}: {content}")
    print("##################################")
    
    
def count_interactions(messages):
    """
    Compte le nombre d'interactions dans la conversation
    """
    return len(messages)


def keep_window_buffer(messages, memory_window):
    """
    Garde la fenêtre de mémoire pour les messages récents
    """
    if count_interactions(messages) >= memory_window: # ce nombre doit être impair pour garder le/les interactions entre l'utilisateur et le LLM
        messages = messages[0:-2] # On garde le system prompt
    return messages

        
def ask_user_input():
    """
    Demande une entrée utilisateur
    """
    return input("Entrez votre message (ou 'exit' pour quitter) : ")


# Fonction pour gérer le streaming de la réponse du LLM
def stream_chat_response(llm, messages):
    """Générateur qui produit les morceaux de réponse un par un."""
    try:
        for chunk in llm.stream(messages):
            yield chunk.content # yield apporte une meilleure gestion de la mémoire et de la performance
    except KeyboardInterrupt:
            print("\nInterruption de l'utilisateur.")
            return
    except Exception as e:
        yield f"[Erreur de communication: {e}]"
        

# Fonction pour afficher la réponse du LLM en streaming
def display_streaming_response(llm, messages):
    """Affiche la réponse du LLM en streaming."""
    print("\nAssistant: \n", end="", flush=True)
    full_response = ""
    
    for text_chunk in stream_chat_response(llm, messages):
        print(text_chunk, end="", flush=True)
        full_response += text_chunk
        time.sleep(0.02)  # Optionnel: simule un délai de frappe naturel
    
    print("\n")
    return full_response 

def parse_json_model_output(json_string:str)->str:
    """
    Nettoie la chaîne JSON pour la rendre valide
    """
    # enlever ce qu'il y a au dessus de '''json
    json_string = json_string.split("```json")[-1]
    
    # Remplace les guillemets simples par des guillemets doubles
    json_string = json_string.replace("```json", '')
    
    # enlever ce qu'il y a en dessous de ```
    json_string = json_string.split("```")[0]
    
    
    # Remplace les caractères de nouvelle ligne par des espaces
    json_string = json_string.replace("```", " ")
    
    
    return json_string

def detect_search_request(response):
    """
    Détecte toutes les demandes de recherche internet dans la réponse du LLM
    et extrait les requêtes de recherche.
    
    Args:
        response (str): Réponse complète du LLM
        
    Returns:
        list: Liste des requêtes de recherche trouvées (vide si aucune)
    """
    import re
    search_pattern = r'SEARCH:\s*"?([^"\n]*)"?'
    # Trouve toutes les occurrences du pattern dans le texte
    matches = re.findall(search_pattern, response)
    
    # Nettoie les requêtes trouvées (enlève les espaces superflus)
    queries = [match.strip() for match in matches if match.strip()]
    
    return queries

def format_response(search_results):
    """
    Formate les résultats de recherche de BraveSearch en un texte lisible.
    
    Args:
        search_results (list): Liste de dictionnaires contenant les résultats de recherche
        
    Returns:
        str: Texte formaté contenant les résultats de recherche
    """
    formatted_text = ""
    
    # Vérifier si search_results est une liste
    if isinstance(search_results, list):
        # Parcourir chaque résultat de recherche
        for i, result in enumerate(search_results, 1):
            title = result.get('title', 'Titre non disponible')
            link = result.get('link', 'Lien non disponible')
            snippet = result.get('snippet', 'Description non disponible')
            
            # Ajouter le résultat formaté au texte
            formatted_text += f"{i}. **{title}**\n"
            formatted_text += f"   URL: {link}\n"
            formatted_text += f"   Description: {snippet}\n\n"
    else:
        # Si ce n'est pas une liste, essayer de traiter comme un autre format
        formatted_text = "Format de résultat non reconnu: " + str(search_results)
    
    return formatted_text