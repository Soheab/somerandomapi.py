from dataclasses import dataclass, field
from typing import Literal, Optional, TYPE_CHECKING

from ...enums import WelcomeTextColor, WelcomeType
from ...internals.endpoints import Premium
from ...types.welcome import WelcomeTextColors
from ..abc import BaseImageModel


__all__ = ("WelcomePremium",)


@dataclass
class WelcomePremium(BaseImageModel):
    """Represents a premium welcome image."""

    _endpoint = Premium.WELCOME

    template: Literal[1, 2, 3, 4, 5, 6, 7] = field(metadata={"range": [1, 7]})
    """The template from a predefined list. Choose a number between 1 and 7."""
    type: WelcomeType
    """The type."""
    username: str
    """The username of the user."""
    avatar_url: str = field(metadata={"alias_of": "avatar"})
    """The avatar URL of the user. Must be .png or .jpg."""
    discriminator: int
    """The discriminator of the user."""
    server_name: str = field(metadata={"alias_of": "guildName"})
    """The server name."""
    member_count: int = field(metadata={"alias_of": "memberCount"})
    """The member count."""
    text_color: WelcomeTextColor = field(metadata={"alias_of": "textcolor"})
    """The text color."""
    key: Optional[str] = field(default=None, repr=False)
    """The key. At least tier 2 is required. Use the free endpoint if you don't have a tier 2 key.
    
    This is required if no tier 2 key was passed to the Client constructor.
    """
    background_url: Optional[str] = field(default=None, repr=False, metadata={"alias_of": "bg"})
    """The background image URL. Requires a tier 2 key."""
    font: Optional[int] = field(default=None, metadata={"range": [1, 10]})
    """The font from a predefined list. Choose a number between 1 and 10."""

    def __post_init__(self):
        self.__class__._validate_types(self, globals(), locals())

    if TYPE_CHECKING:

        @classmethod
        def from_dict(
            cls,
            *,
            type: Literal["join", "leave"],
            username: str,
            avatar: str,
            discriminator: int,
            guildName: str,
            memberCount: int,
            textcolor: WelcomeTextColors,
            key: Optional[str] = None,
            bg: Optional[str] = None,
            font: Optional[int] = None,
        ):
            ...
