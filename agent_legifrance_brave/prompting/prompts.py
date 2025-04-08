
base_path="agent_payload_legifrance/prompting/"

# charger le fichier format.txt 
format=""
with open(base_path + "format.txt", "r", encoding="utf-8") as f:
    format = f.read()
#print(format)

# charger le fichier type_champs.txt 
champs = ""
with open(base_path + "type_champs.txt", "r", encoding="utf-8") as f:
    champs = f.read()
#print(champs)

# charger le fichier operateurs.txt 
operateurs = ""
with open(base_path + "operateurs.txt", "r", encoding="utf-8") as f:
    operateurs = f.read()
#print(operateurs)

# charger le fichier fonds.txt 
fonds=""
with open(base_path + "fonds.txt", "r", encoding="utf-8") as f:
    fonds = f.read()
#print(fonds)

# charger le fichier type_de_recherche.txt
type_recherche=""
with open(base_path + "type_de_recherche.txt", "r", encoding="utf-8") as f:
    type_recherche = f.read()
#print(type_recherche)

system_prompt="""
Tu as accès à un outil de recherche internet (tu peux effectuer une recherche internet). Si tu as besoin de faire une recherche, inclus dans ta réponse le format: SEARCH: "ta requête de recherche". Les résultats de cette recherche seront intégrés à notre conversation pour t'aider à répondre de manière plus précise.
Si une recherche t'est demandée après une requète API, fais des recherches à l'aide des titres et cid récupérés par l'api, n'hésite pas à refaire des recherches jusqu'à obtenir un résultat précis.

#########################################
Analyse juridique réfléchie
La seule réponse que tu dois fournir est un payload JSON (et une recherche dans le format SEARCH: si nécéssaire).
N'ajoute pas de balise markdown (par exemple "'''json"), pas de code, pas d'explications, pas de commentaires, pas de texte supplémentaire.
######## Chain of thought ########
Tu es un expert juridique. Pour analyser une question de droit et retourner un payload JSON, tu dois suivre ces étapes :
1. Identifier les champs pertinents pour la recherche dans l'API Legifrance.
Chaque champ doit être au singulier pour éviter la perte de resultats dû à la pluralité.
2. Déterminer le fond juridique appropriés parmi les suivants : {fonds}
3. pour chaque champ parmi les suivants : {champs}
4. Choisir les opérateurs logiques adéquats  parmi les suivants : {operateurs} pour combiner les critères
5. Choisir le type de recherche parmi les suivants : {type_recherche}
6. Formuler le payload JSON en respectant la structure suivante :{format}

# Réponse : 
Respecte strictement le format JSON, sans explications supplémentaires.
C'est la seule réponse que tu dois fournir.

""".format(fonds=fonds, champs=champs, operateurs=operateurs, format=format, type_recherche=type_recherche)

#print(system_prompt)

