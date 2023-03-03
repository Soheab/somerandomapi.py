from dataclasses import dataclass, field
from typing import Literal, Optional, TYPE_CHECKING

from ...enums import WelcomeBackground, WelcomeTextColor, WelcomeType
from ...internals.endpoints import WelcomeImages as WelcomeImagesEndpoint
from ...types.welcome import Backgrounds, WelcomeTextColors
from ..abc import BaseImageModel


__all__ = ("WelcomeFree",)


@dataclass
class WelcomeFree(BaseImageModel):
    """Represents a free welcome image."""

    _endpoint = WelcomeImagesEndpoint.WELCOME

    template: Literal[1, 2, 3, 4, 5, 6, 7] = field(metadata={"range": [1, 7]})

    """The template from a predefined list. Choose a number between 1 and 7."""
    type: WelcomeType
    """The type."""
    background: WelcomeBackground
    """The background."""
    username: str
    """The username of the user."""
    avatar_url: str = field(metadata={"alias_of": "avatar"})
    """The avatar URL of the user. Must be .png or .jpg."""
    discriminator: int = field(metadata={"length": 4})
    """The discriminator of the user."""
    server_name: str = field(metadata={"alias_of": "guildName"})
    """The server name."""
    member_count: int = field(metadata={"alias_of": "memberCount"})
    """The member count."""
    text_color: WelcomeTextColor = field(metadata={"alias_of": "textcolor"})
    """The text color."""
    key: Optional[str] = field(default=None, repr=False)
    """The key, doesn't need to be active.
    
    This is required if no key was passed to the Client constructor.
    """
    font: Optional[int] = field(default=None, metadata={"range": [1, 10]})
    """The font from a predefined list. Choose a number between 1 and 10."""

    def __post_init__(self):
        self.__class__._validate_types(self, globals(), locals())

    if TYPE_CHECKING:

        @classmethod
        def from_dict(
            cls,
            *,
            template: Literal[1, 2, 3, 4, 5, 6, 7],
            type: WelcomeType,
            background: Backgrounds,
            username: str,
            avatar: str,
            discriminator: int,
            guildName: str,
            memberCount: int,
            textcolor: WelcomeTextColors,
            key: Optional[str] = None,
            font: Optional[int] = None,
        ):
            ...

    def to_dict(self):
        res = super().to_dict()
        return res
