import pytest 
from unittest.mock import patch, MagicMock


# à appeler avec 'python -m tests.Conversation.tests_utils_conversation '

# fichier à tester
from Conversation.utils_conversation import ( 
                                                display_context,
                                                count_interactions,
                                                keep_window_buffer,
                                                demander_entree_utilisateur,
                                                stream_chat_response,
                                                display_streaming_response, 
                                                )

def test_count_interactions():
    "teste la fonction count_interactions"
    messages = [("user", "Hey"), ("assistant", "Hello")]
    assert count_interactions(messages) == 2 , "Le nombre d'interactions doit être 2."
    
def test_keep_window_buffer_when_overflow():
    "teste la fonction keep_window_buffer lorsque le nombre de messages dépasse la limite"
    messages = [("system", "Prompt initial")] + [("user", f"msg {i}") for i in range(6)]
    result = keep_window_buffer(messages, memory_window=5)
    # On vérifie que les derniers messages sont supprimés si le seuil est dépassé
    assert result == messages[0:-2], "Les messages doivent être tronqués pour respecter la limite de mémoire."


def test_keep_window_buffer_when_within_limit():
    "Teste la fonction keep_window_buffer lorsque le nombre de messages est inférieur à la limite"
    messages = [("system", "Prompt initial")] + [("user", f"msg {i}") for i in range(2)]
    result = keep_window_buffer(messages, memory_window=5)
    # Aucun changement car en-dessous de la limite
    assert result == messages ,"Les messages doivent rester inchangés car en-dessous de la limite de mémoire."
    
    
def test_display_context(capsys):
    """
    Vérifie que display_context affiche bien les messages dans le bon format.
    """
    messages = [("user", "Bonjour"), ("assistant", "Salut !")]
    display_context(messages)
    output = capsys.readouterr().out # Pour capturer la sortie console
    assert "Contexte actuel" in output
    assert "user: Bonjour" in output
    assert "assistant: Salut !" in output

@patch("builtins.input", return_value="hello")
def test_demander_entree_utilisateur(mock_input):
    """
    Vérifie que l'entrée utilisateur est bien captée.
    """
    assert demander_entree_utilisateur() == "hello"


def test_stream_chat_response():
    """
    Vérifie que stream_chat_response envoie les bons morceaux de réponse.
    """
    mock_llm = MagicMock()
    mock_llm.stream.return_value = [MagicMock(content="Hello "), MagicMock(content="world!")]
    messages = [("user", "Salut")]
    result = list(stream_chat_response(mock_llm, messages))
    assert result == ["Hello ", "world!"]


if __name__ == "__main__":
    pytest.main([__file__])



