
# Hermine Chatbot Agent

## LLM
### Initialisation du LLM
- **Par défaut** : `mistral`
- **Scripts** :
    - `init_llm.py` : Initialisation d'un LLM.
    - `exemple_utilisation.py` : Exemple d'utilisation du LLM.
    - `env_variable_loader.py` : Chargement des variables d'environnement pour centraliser leur récupération.

## Conversation
### Mise en place d'une conversation utilisateur/LLM avec mémoire
- **Script** :
    - `conversation.py` : Implémente une conversation avec affichage asynchrone et streaming de la réponse LLM.

## Tests
- **Conversation** :
    - `Conversation/tests_conversation.py` : Tests unitaires pour la partie conversation.
- **LLM** :
    - `LLM/tests_init_llm_and_env_variable.py` : Tests unitaires pour l'initialisation du LLM choisi.

## Lancer la conversation
```bash
python -m Conversation.conversation
```

## Points de réflexion
- **Pattern Factory** : Utile pour des changements rapides de technologies.
- **Prompt Caching** : Étudier les avantages et inconvénients de Redis avec un `SequenceMatcher`.

## Notes importantes
- La mémoire sur LangChain est dépréciée dans les nouvelles versions.
- Utiliser les mémoires LangGraph : [Documentation LangChain](https://python.langchain.com/docs/versions/migrating_memory/)
