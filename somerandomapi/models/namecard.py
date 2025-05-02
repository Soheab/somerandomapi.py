from ..internals.endpoints import CanvasMisc
from .abc import BaseImageModel, attribute

__all__ = ("GenshinNamecard",)


class GenshinNamecard(BaseImageModel):
    """Represents a genshin namecard."""

    __endpoint__ = CanvasMisc.GENSHIN_NAMECARD

    avatar_url: str = attribute(data_name="avatar")
    """:class:`str`: The avatar URL of the user. Must be .png or .jpg."""
    """The avatar URL of the user. Must be .png or .jpg."""
    birthday: str
    """The birthday, dd/mm/yyyy"""
    username: str
    """The username"""
    description: str | None
    """The description"""
