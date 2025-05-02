from ..internals.endpoints import CanvasMisc
from .abc import BaseImageModel, attribute

__all__ = ("YoutubeComment",)


class YoutubeComment(BaseImageModel):
    """Represents a Youtube Comment."""

    __endpoint__ = CanvasMisc.YOUTUBE_COMMENT

    username: str = attribute(max_length=25)
    """The username of the user. Max 25 characters."""
    avatar_url: str = attribute(data_name="avatar")
    """The avatar URL of the user. Must be .png or .jpg."""
    text: str = attribute(max_length=1000, data_name="comment")
    """The text of the comment. Max 1000 characters."""
