from somerandomapi.enums import WelcomeBackground, WelcomeTextColor, WelcomeType
from somerandomapi.models.welcome.free import WelcomeFree


def test_welcome_free_model() -> None:
    model = WelcomeFree(
        template=1,
        type=WelcomeType.JOIN,
        background=WelcomeBackground.SPACE,
        username="user",
        avatar_url="https://example.com/avatar.png",
        server_name="Server",
        member_count=42,
        text_color=WelcomeTextColor.WHITE,
    )
    data = model.to_dict()
    assert data["avatar"] == "https://example.com/avatar.png"
    assert data["guildName"] == "Server"
    assert WelcomeFree.from_dict(data).member_count == "42"
