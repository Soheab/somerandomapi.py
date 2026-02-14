from somerandomapi.models.chatbot import ChatbotResult


def test_chatbot_result_model() -> None:
    model = ChatbotResult(message="hello", response="world")
    assert model.message == "hello"
    assert str(model) == "world"
    assert len(model) == 5

