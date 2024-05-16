from dataclasses import dataclass, field
from typing import Literal, Optional, TYPE_CHECKING

import logging

from ...enums import WelcomeBackground, WelcomeTextColor, WelcomeType
from ...internals.endpoints import WelcomeImages as WelcomeImagesEndpoint
from ...types.welcome import Backgrounds, WelcomeTextColors
from ..abc import BaseImageModel


__all__ = ("WelcomeFree",)

_log = logging.getLogger("somerandomapi.welcome.free")


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
    server_name: str = field(metadata={"alias_of": "guildName"})
    """The server name."""
    member_count: int = field(metadata={"alias_of": "memberCount"})
    """The member count."""
    text_color: WelcomeTextColor = field(metadata={"alias_of": "textcolor"})
    """The text color."""
    discriminator: Optional[int] = field(default=None, metadata={"min_length": 1, "max_length": 4})
    """The discriminator of the user.
    
    Will be stripped if equal to 0
    """
    key: Optional[str] = field(default=None, repr=False)
    """The key, doesn't need to be active.
    
    This is required if no key was passed to the Client constructor.
    """
    font: Optional[Literal[0, 1, 2, 3, 4, 5, 6, 7]] = field(default=None, metadata={"range": [0, 10]})
    """The font from a predefined list. Choose a number between 0 and 7.
    
    .. versionchanged:: 0.0.8
        The library sets the font to 7 if it's greater than 8 as the API only accepts a range of 0-7 now.
    """

    def __post_init__(self):
        # prevent breaking changes
        if self.font is not None:
            if self.font > 8:
                _log.debug(
                    "Preventing breaking changes for font. Changed from %s to %s as the API takes a range of 0-7 now.",
                    self.font,
                    "7",
                )

                self.font = 7

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
            guildName: str,
            memberCount: int,
            textcolor: WelcomeTextColors,
            discriminator: Optional[int] = None,
            key: Optional[str] = None,
            font: Optional[int] = None,
        ): ...

    def to_dict(self):
        res = super().to_dict()
        return res
