from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ..internals.endpoints import CanvasMisc
from .abc import BaseImageModel


__all__ = ("YoutubeComment",)


@dataclass
class YoutubeComment(BaseImageModel):
    """Represents a Youtube Comment."""

    _endpoint = CanvasMisc.YOUTUBE_COMMENT

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

    def __post_init__(self):
        self.__class__._validate_types(self, globals(), locals())
