from __future__ import annotations
from typing import TYPE_CHECKING, Any, ClassVar, Literal, Optional, Tuple, Optional

from dataclasses import dataclass, field

from .abc import BaseModel
from ..internals.endpoints import CanvasMisc

if TYPE_CHECKING:
    from ..models.image import Image


__all__: Tuple[str, ...] = ("Tweet",)


@dataclass
class Tweet(BaseModel):
    """Represents a tweet."""

    _endpoint = CanvasMisc.TWEET
    _image: Image = field(init=False)

    display_name: str = field(metadata={"max_length": 32, "alias_of": "displayname"})
    """The display name of the user. Max 32 characters."""
    username: str = field(metadata={"max_length": 15})
    """The username of the user. Max 15 characters."""
    avatar_url: str = field(metadata={"alias_of": "avatar"})
    """The avatar URL of the user. Must be .png or .jpg."""
    text: str = field(metadata={"max_length": 1000, "alias_of": "comment"})
    """The text of the tweet. Max 1000 characters."""
    replies: Optional[int]
    """The amount of replies the tweet is supposed to have."""
    likes: Optional[int]
    """The amount of likes the tweet is supposed to have."""
    retweets: Optional[int]
    """The amount of retweets the tweet is supposed to have."""
    theme: Optional[Literal["light", "dim", "dark"]] = field(
        default="light", metadata={"must_be_one_of": ["light", "dim", "dark"]}
    )
    """The theme of the tweet. Defaults to "light"."""

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

    @property
    def image(self) -> Image:
        """The image of the tweet.

        Returns
        -------
        :class:`Image`
                The image of the tweet.
        """
        return self._image
