from __future__ import annotations
from typing import TYPE_CHECKING, Literal, Optional, Tuple, Optional

from dataclasses import dataclass, field

from ...internals.endpoints import Premium
from ..abc import BaseModel
from ...enums import WelcomeType, WelcomeTextColor
from ...types.welcome import WelcomeTextColors

if TYPE_CHECKING:
    from ...models.image import Image

__all__: Tuple[str, ...] = ("WelcomePremium",)


@dataclass
class WelcomePremium(BaseModel):
    """Represents a rank card."""

    _endpoint = Premium.WELCOME

    _image: Image = field(init=False)

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
    """The text color. Must be one of: red, orange, yellow, green, blue, indigo, purple, purple, pink, black, white."""
    key: Optional[str] = field(default=None, repr=False)
    """The key. At least tier 2 is required. Use the free endpoint if you don't have a tier 2 key.
    
    This is required if no tier 2 key was passed to the Client constructor.
    """
    background_url: Optional[str] = field(default=None, repr=False, metadata={"alias_of": "bg"})
    """The background image URL. Requires a tier 2 key."""
    font: Optional[int] = field(default=None, metadata={"range": [1, 10]})
    """The font from a predefined list. Choose a number between 1 and 10."""

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

    @property
    def image(self) -> Image:
        """The image of the tweet.

        Returns
        -------
        :class:`Image`
            The image of the tweet.
        """
        return self._image
