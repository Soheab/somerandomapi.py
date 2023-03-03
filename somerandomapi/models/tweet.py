from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional, TYPE_CHECKING

from ..internals.endpoints import CanvasMisc
from .abc import BaseImageModel


__all__ = ("Tweet",)


@dataclass
class Tweet(BaseImageModel):
    """Represents a tweet."""

    _endpoint = CanvasMisc.TWEET

    display_name: str = field(metadata={"max_length": 32, "alias_of": "displayname"})
    """:class:`str`: The display name of the user. Max 32 characters."""
    username: str = field(metadata={"max_length": 15})
    """:class:`str`: The username of the user. Max 15 characters."""
    avatar_url: str = field(metadata={"alias_of": "avatar"})
    """:class:`str`: The avatar URL of the user. Must be .png or .jpg."""
    text: str = field(metadata={"max_length": 1000, "alias_of": "comment"})
    """:class:`str`: The text of the tweet. Max 1000 characters."""
    replies: Optional[int]
    """Optional[:class:`int`]: The amount of replies the tweet is supposed to have."""
    likes: Optional[int]
    """Optional[:class:`int`]: The amount of likes the tweet is supposed to have."""
    retweets: Optional[int]
    """Optional[:class:`int`]: The amount of retweets the tweet is supposed to have."""
    theme: Optional[Literal["light", "dim", "dark"]] = "light"
    """Optional[Literal["light", "dim", "dark"]]: The theme of the tweet. Defaults to "light"."""

    if TYPE_CHECKING:

        @classmethod
        def from_dict(
            cls,
            *,
            theme: Optional[Literal["light", "dim", "dark"]] = "light",
            displayname: str,
            username: str,
            avatar: str,
            comment: str,
            replies: Optional[int],
            likes: Optional[int],
            retweets: Optional[int],
        ):
            ...

    def __post_init__(self):
        self.__class__._validate_types(self, globals(), locals())
