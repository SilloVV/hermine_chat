'Fichier de définition des outils pour la recherche sur Brave'

from langchain.tools import BaseTool
from langchain_community.tools import BraveSearch

def recherche_brave(BaseTool):
    description = ""
    name=""
    
    def _run(query: str, nombre_resultats: int = 5) -> str:
        """
        Fonction interne pour exécuter la recherche sur Brave.
        """
        
        return "Résultats de la recherche sur Brave pour : " + query
    