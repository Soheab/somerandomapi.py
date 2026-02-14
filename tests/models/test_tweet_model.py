from somerandomapi.enums import TweetTheme
from somerandomapi.models.tweet import Tweet


def test_tweet_model_defaults_and_mapping() -> None:
    model = Tweet(display_name="User", username="usr", avatar_url="https://example.com/avatar.png", text="Hello")
    assert model.theme == TweetTheme.LIGHT
    data = model.to_dict()
    assert data["displayname"] == "User"
    assert data["avatar"] == "https://example.com/avatar.png"
    assert data["comment"] == "Hello"

