from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

from dataclasses import dataclass, field

from .abc import BaseModel

from ..internals.endpoints import CanvasMisc

if TYPE_CHECKING:
    from ..models.image import Image


__all__: Tuple[str, ...] = ("YoutubeComment",)


@dataclass
class YoutubeComment(BaseModel):
    """Represents a Youtube Comment."""

    _endpoint = CanvasMisc.YOUTUBE_COMMENT

    _image: Image = field(init=False)

    username: str = field(metadata={"max_length": 25})
    """The username of the user. Max 25 characters."""
    avatar_url: str = field(metadata={"alias_of": "avatar"})
    """The avatar URL of the user. Must be .png or .jpg."""
    text: str = field(metadata={"max_length": 1000, "alias_of": "comment"})
    """The text of the tweet. Max 1000 characters."""

    if TYPE_CHECKING:

        @classmethod
        def from_dict(
            cls,
            *,
            username: str,
            avatar: str,
            comment: str,
        ):
            ...

    @property
    def image(self) -> Image:
        """The image of the youtube comment.

        Returns
        -------
        :class:`Image`
            The image of the youtube comment.
        """
        return self._image
