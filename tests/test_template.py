import pytest 

# à appeler avec 'python -m tests.' ou 'pytest tests/<path>.py -W ignore'

## si la clé n'est pas bonne, on doit avoir une erreur
def test_function_return_answer() -> bool:
    """
    teste quelque chose
    """
    result = function(param1, param2)
    assert result is False, "Le résultat doit être ..."
    

if __name__ == "__main__":
    pytest.main([__file__])
