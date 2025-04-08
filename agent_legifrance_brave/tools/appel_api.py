import requests
import os
from dotenv import load_dotenv
from typing import Dict

# Chargement des variables d'environnement
load_dotenv()

# Configuration des identifiants API Legifrance Sandbox
LEGIFRANCE_CLIENT_ID = os.getenv("LEGIFRANCE_CLIENT_ID")
LEGIFRANCE_CLIENT_SECRET = os.getenv("LEGIFRANCE_CLIENT_SECRET")
LEGIFRANCE_BASE_URL = "https://sandbox-api.piste.gouv.fr/dila/legifrance/lf-engine-app"
LEGIFRANCE_OAUTH_URL = "https://sandbox-oauth.piste.gouv.fr/api/oauth/token"


def obtenir_token_legifrance():
    """Obtient un token OAuth pour l'API Legifrance."""
    url = LEGIFRANCE_OAUTH_URL
    
    payload = {
        "grant_type": "client_credentials",
        "client_id": LEGIFRANCE_CLIENT_ID,
        "client_secret": LEGIFRANCE_CLIENT_SECRET,
        "scope": "openid"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Erreur d'authentification: {response.status_code} - {response.text}")
        return None


# outil Langchain d'appel à l'endpoint search legifrance
def api_call(Payload: dict):
    """Appel à l'endpoint /search de l'api Legifrance"""
    name="legifrance_search"
    description="Outil d'appel à l'endpoint /search de l'API Legifrance pour la recherche de textes législatifs."
    
    token = obtenir_token_legifrance()
    
    if not token:
        return "Échec de connexion à Legifrance (échec d'obtention du token)"
    
    #print(f"INFO : Token obtenu avec succès !")
    
    # Test de requête simple - recherche de texte
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    
    # Requête simple pour rechercher le Code civil
    payload = Payload
    
    # test ping pong
    pong = requests.get(f"{LEGIFRANCE_BASE_URL}/search/ping", headers=headers)

    if pong.status_code == 500:
        print("INFO: L'API Legifrance est en ligne !")
    else:
        raise Exception("ERREUR: L'API Legifrance ne répond pas.")
    
    response = requests.post(f"{LEGIFRANCE_BASE_URL}/search", headers=headers, json=payload)
    
    if response.status_code == 200:
        resultats = response.json()
        titres = []
        cids = []
        if resultats.get('results') is None:
            print("INFO: Aucun résultat trouvé.")
            return []
        for resultat in resultats.get('results', []):
            #print("INFO : résultats trouvés !")
            for titre in resultat.get('titles', []):
                print("INFO: -> " + titre.get('title', 'Titre non disponible') + "-> " + titre.get('cid', 'CID non disponible'))
                titres.append(titre.get('title', 'Titre non disponible'))
                cids.append(titre.get('cid', 'CID non disponible'))
        print("INFO: Requête réussie !")
        return titres, cids
    else:
        print(f"Erreur lors de la requête: {response.status_code} - {response.text}")
        return f"Échec de la requête à Legifrance: code {response.status_code}"


## utilisation de l'outil
if __name__ == "__main__":

    print("Test de l'API Legifrance")
    print("====================================")

    print(api_call({
        "recherche": {
            "champs": [
                {
                    "typeChamp": "TITLE",
                    "criteres": [
                        {
                            "typeRecherche": "TOUS_LES_MOTS_DANS_UN_CHAMP",
                            "valeur": "Paris",
                            "operateur": "OU"
                        },
                        {
                            "typeRecherche": "TOUS_LES_MOTS_DANS_UN_CHAMP",
                            "valeur": "accès",
                            "operateur": "ET"
                        }
                    ],
                    "operateur": "OU"
                }
            ],
            "pageNumber": 1,
            "pageSize": 15,
            "sort": "PERTINENCE"
        },
        "fond": "ALL"
    }))