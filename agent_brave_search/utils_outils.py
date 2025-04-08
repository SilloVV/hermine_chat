

# formatter le réponse 
def format_response(response_parts):
    """
    Formate une réponse composée de parties de texte et de références
    """
    full_text = ""
    references = []
    
    for part in response_parts:
        if part['type'] == 'text':
            full_text += part['text']
        elif part['type'] == 'reference':
            # Ajoute les références à la liste
            references.extend(part['reference_ids'])
            # Si vous voulez inclure les références dans le texte, décommentez la ligne suivante
            # full_text += ", ".join(part['reference_ids'])
    
    return {
        "formatted_text": full_text,
        "references": references
    }
