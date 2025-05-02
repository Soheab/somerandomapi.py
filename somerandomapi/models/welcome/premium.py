from typing import Literal

from ...enums import WelcomeTextColor, WelcomeType
from ...internals.endpoints import Premium
from ..abc import BaseImageModel, attribute

__all__ = ("WelcomePremium",)


class WelcomePremium(BaseImageModel):
    """Represents a premium welcome image."""

    __endpoint__ = Premium.WELCOME

    template: Literal[1, 2, 3, 4, 5, 6, 7] = attribute(range=(1, 7))
    """The template from a predefined list. Choose a number between 1 and 7."""
    type: WelcomeType
    """The type."""
    username: str
    """The username of the user."""
    avatar_url: str = attribute(data_name="avatar")
    """The avatar URL of the user. Must be .png or .jpg."""
    server_name: str = attribute(data_name="guildName")
    """The server name."""
    member_count: int = attribute(data_name="memberCount")
    """The member count."""
    text_color: WelcomeTextColor = attribute(data_name="textcolor")
    """The text color."""
    discriminator: int | None = attribute(default=None, min_length=1, max_length=4, forced_type=str)
    """The discriminator of the user.
    
    Will be stripped if equal to 0
    """
    background_url: str | None = attribute(default=None, repr=False, data_name="bg")
    """The background image URL."""
    font: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None = attribute(default=None, range=(0, 7))
    """The font from a predefined list. Choose a number between 0 and 7.
    
    .. versionchanged:: 0.1.0
        This takes a range of 0-7 now instead of 0-8.
    """
