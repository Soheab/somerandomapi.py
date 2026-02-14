from somerandomapi.models.namecard import GenshinNamecard


def test_genshin_namecard_model() -> None:
    model = GenshinNamecard(
        avatar_url="https://example.com/avatar.png",
        birthday="01/01/2000",
        username="user",
        description="desc",
    )
    data = model.to_dict()
    assert data["avatar"] == "https://example.com/avatar.png"
    restored = GenshinNamecard.from_dict(data)
    assert restored.avatar_url == model.avatar_url

