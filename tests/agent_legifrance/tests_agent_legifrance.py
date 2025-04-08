import pytest 

from agent_legifrance import utils_conversation

# fonction de test de la fonction clean_json_model_output

def test_clean_json_model_output():
    """
    Teste la fonction clean_json_model_output pour s'assurer qu'elle nettoie correctement les chaînes JSON.
    """
    json_string = """
```json
```
"""
    result = utils_conversation.clean_json_model_output(json_string)
    print(result)
    assert result == """\n\n \n""", "La chaîne JSON doit être nettoyée correctement."

if __name__ == "__main__":
    pytest.main([__file__])
