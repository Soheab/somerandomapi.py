from __future__ import annotations
from typing import TYPE_CHECKING, Literal, Optional, Tuple, Optional

from dataclasses import dataclass, field

from ...internals.endpoints import WelcomeImages as WelcomeImagesEndpoint
from ..abc import BaseModel
from ...enums import WelcomeType, WelcomeBackground, WelcomeTextColor
from ...types.welcome import WelcomeTextColors, Backgrounds

if TYPE_CHECKING:
    from ...models.image import Image

__all__: Tuple[str, ...] = ("WelcomeFree",)


@dataclass
class WelcomeFree(BaseModel):
    """Represents a rank card."""

    _endpoint = WelcomeImagesEndpoint.WELCOME

    _image: Image = field(init=False)

    type: WelcomeType
    """The type."""
    background: WelcomeBackground
    """The background."""
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
    """The text color. Must be one of: red, orange, yellow, green, blue, indigo, purple, purple, pink, black, white."""
    key: Optional[str] = field(default=None, repr=False)
    """The key, doesn't need to be active.
    
    This is required if no key was passed to the Client constructor.
    """
    font: Optional[int] = field(default=None, metadata={"range": [1, 10]})
    """The font from a predefined list. Choose a number between 1 and 10."""

    if TYPE_CHECKING:

        @classmethod
        def from_dict(
            cls,
            *,
            type: Literal["join", "leave"],
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
        res.pop("background", None)
        return res

    @property
    def image(self) -> Image:
        """The image of the tweet.

        Returns
        -------
        :class:`Image`
            The image of the tweet.
        """
        return self._image
