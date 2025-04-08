# import=outils 
from LLM.env_variable_loader import load_var_env
from langchain_community.tools import BraveSearch
from agent_brave_search.utils_outils import format_response
SEARCH_API_KEY_NAME = load_var_env("SEARCH_API_KEY_NAME")
SEARCH_API_KEY_VALUE=load_var_env(SEARCH_API_KEY_NAME) 
NUMBER_OF_RESULTS = 5 # nombre de résultats à retourner




if __name__ == "__main__":
    # exemple d'implémentation de l'outil de recherche
    search_tool = BraveSearch.from_api_key(
    api_key=SEARCH_API_KEY_VALUE, 
    search_kwargs={"count": NUMBER_OF_RESULTS}
    )
    
    # Exemple d'utilisation de la classe SearchTool
    query = "What is the capital of France?"
    result = search_tool.invoke(query)
    print(result)
    formatted_result = format_response(result)
    print(formatted_result)