import pytest

from somerandomapi.models.rankcard import Rankcard


def test_rankcard_model_basics() -> None:
    model = Rankcard(
        template=1,
        username="user",
        avatar_url="https://example.com/avatar.png",
        level=10,
        current_xp=100,
        needed_xp=1000,
        background_color="#00ff00",
        text_color="ffffff",
    )
    assert model.background_color == "00ff00"
    assert model.text_color == "ffffff"
    data = model.to_dict()
    assert data["avatar"] == "https://example.com/avatar.png"
    assert data["template"] == "1"


def test_rankcard_model_invalid_colors() -> None:
    with pytest.raises(ValueError):
        Rankcard(
            template=1,
            username="user",
            avatar_url="https://example.com/avatar.png",
            level=10,
            current_xp=100,
            needed_xp=1000,
            background_color="zzzzzz",
        )

