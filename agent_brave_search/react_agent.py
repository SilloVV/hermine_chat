
# LLM 
from LLM.init_llm import initialize_llm
from LLM.env_variable_loader import load_var_env

MODEL_NAME="mistral-large-latest" # voir : https://docs.mistral.ai/getting-started/models/models_overview/ pour d'autres modèles

# import des prompts 
from .prompting.prompts import system_prompt

# environnement
SEARCH_API_KEY_NAME = load_var_env("SEARCH_API_KEY_NAME")
SEARCH_API_KEY_VALUE=load_var_env(SEARCH_API_KEY_NAME) 
NUMBER_OF_RESULTS = 5 # nombre de résultats à retourner

# import des outils de recherche
from langchain_community.tools import BraveSearch

# import des utils 
from agent_brave_search.utils_outils import format_response

search_tool = BraveSearch.from_api_key(
    api_key=SEARCH_API_KEY_VALUE, 
    search_kwargs={"count": NUMBER_OF_RESULTS}
    )
 
# React agent 
from langgraph.prebuilt import create_react_agent

def main():
    llm = initialize_llm(MODEL_NAME, temperature=0.1, max_output_tokens=1000)
    
    # créer l'agent react : Reason and Act
    agent= create_react_agent(llm, [search_tool], prompt=system_prompt)
    
    # Afficher le message de bienvenue
    print("Bienvenue dans la conversation avec le LLM !")
    print("Tapez 'exit' pour quitter.")
    
    user_input = input("Entrez votre question : ")
    all_responses = []
    
    for step in agent.stream(
        {"messages": user_input},
        stream_mode="values",
    ):
        
        # Accéder au dernier message et l'ajouter à notre liste
        last_message = step["messages"][-1].pretty_print()
        all_responses.append(last_message)
        
        
    final_response = all_responses[-1]
    # Si vous voulez accéder au contenu du message
    if hasattr(final_response, "content"):
        if isinstance(final_response.content, list):
            # Traiter le contenu structuré
            formatted_result = format_response(final_response.content)
            print(formatted_result["formatted_text"])
        else:
            # Si le contenu est une simple chaîne
            print(final_response.content)
    else:
        # Fallback si la structure est différente
        print("Format de réponse non standard:", final_response)

if __name__ == "__main__":
    main()
