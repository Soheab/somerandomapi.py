from somerandomapi.models.youtube_comment import YoutubeComment


def test_youtube_comment_model() -> None:
    model = YoutubeComment(username="user", avatar_url="https://example.com/avatar.png", text="Great video")
    data = model.to_dict()
    assert data["avatar"] == "https://example.com/avatar.png"
    assert data["comment"] == "Great video"
    assert YoutubeComment.from_dict(data).text == "Great video"

