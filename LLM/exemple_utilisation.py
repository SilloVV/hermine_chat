from init_llm import initialize_llm

MODEL_NAME="mistral-large-latest" # voir : https://docs.mistral.ai/getting-started/models/models_overview/ pour d'autres modèles

llm = initialize_llm(MODEL_NAME, temperature=0.2,max_output_tokens=50) 

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    (
        "human",
        "I love programming."
    )
]

ai_msg = llm.invoke(messages)
print(ai_msg)

# en streaming : on peut l'arreter à tout moment avec Ctrl+C ou autre interruption
# " le streaming est au niveau de l'API, il découpe la réponse en plusieurs morceaux et les envoie au fur et à mesure"
# l'affichage se fait en dynamique , plus intéressant pour attendre la réponse coté utilisatueur 
for chunk in llm.stream(messages):
    print(chunk.content, end="", flush=True)
    
# Cas utiles 
## 1. recupérer uniquement la réponse du llm
print("##################################")
print(f"\nRéponse du LLM :")
print(ai_msg.content)
## 2. récupérer les tokens utilises en entrée
print("##################################")
print(f"\ntokens utilisés en entrée :")
print(ai_msg.usage_metadata['input_tokens'])
## 3. récupérer les tokens utilises en sortie
print("##################################")
print(f"\ntokens utilisés en sortie :")
print(ai_msg.usage_metadata['output_tokens'])
## 4. récupérer les tokens utilises au total
print("##################################")
print(f"\ntokens utilisés au total :")
print(ai_msg.usage_metadata['total_tokens'])
    