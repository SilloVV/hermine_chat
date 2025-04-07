
--> LLM
'Initialisation du LLM': mistral par défaut 
- init_llm.py : Afin d'initialiser un LLM
- exemple_utilisation.py : exemple d'utilisation du LLM
- tests_init_llm_and_env_variable.py : tests unitaires 
- env_variable_loader.py : permet de charger les variables d'environnement: cela permet de centraliser la récupération de variables d'environnement
  
--> Conversation 
'Appel du LLM pour la mise en place d'une conversation utilisateur/LLM avec mémoire de conversation'
- conversation.py : mise en place de la conversation 
  - > implémente une conversation via un affichage asynchrone et en streaming de la réponse llm 
- tests_conversation.py : tests unitaires

Pour lancer la conversation : 'python -m Conversation.conversation'

-> Réflechir au pattern Factory : utile pour des changement rapides de technologies
-> Réflechir aux méthodes de prompt caching : Redis: pro & cons avec un SequenceMatcher

### Il faut faire attention car la mémoire sur langchain est dépréciée dans les nouvelles versions
### Il faut utiliser les mémoires Langgraph :https://python.langchain.com/docs/versions/migrating_memory/
