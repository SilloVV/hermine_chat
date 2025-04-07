import pytest 

# fichier à tester
from LLM.init_llm import try_api_key
from LLM.env_variable_loader import load_var_env

# à appeler avec 'python -m tests.LLM.tests_init_llm_and_env_variable_loader'

## si la clé n'est pas bonne, on doit avoir une erreur
def test_try_api_key_return_False() -> bool:
    """
    teste si la clé est correcte
    """
    API_key = "not_a_good_key"
    result = try_api_key(API_key)
    assert result is False, "La clé API doit ne pas être valide."


# si la variable d'environnement est bien présente dans .env, on doit avoir une réponse True
def test_load_var_env_return_True() -> bool:
    """
    teste si la clé est correcte
    """
    # on charge la variable d'environnement
    env_var = load_var_env("test_key")
    if env_var == "test_key":
        result = True
    else:
        result = False
    assert result is True, "La variable d'environnement doit être trouvée."


# si la variable d'environnement n'est pas présente dans .env, on doit avoir une erreur
def test_load_var_env_return_False() -> bool:
    """
    teste si la clé est correcte
    """
    # on charge la variable d'environnement
    try:
       env_var = load_var_env("not_a_good_key")
       result = True
    except ValueError:
        result = False
    assert result is False, "La variable d'environnement ne doit pas être trouvée."


if __name__ == "__main__":
    pytest.main([__file__])