from somerandomapi.enums import WelcomeTextColor, WelcomeType
from somerandomapi.models.welcome.premium import WelcomePremium


def test_welcome_premium_model() -> None:
    model = WelcomePremium(
        template=1,
        type=WelcomeType.JOIN,
        username="user",
        avatar_url="https://example.com/avatar.png",
        server_name="Server",
        member_count=42,
        text_color=WelcomeTextColor.WHITE,
        background_url="https://example.com/bg.png",
    )
    data = model.to_dict()
    assert data["bg"] == "https://example.com/bg.png"
    assert data["guildName"] == "Server"
    restored = WelcomePremium.from_dict(data)
    assert restored.username == "user"

