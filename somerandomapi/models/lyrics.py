from ..internals.endpoints import Base
from .abc import BaseModel

__all__ = ("Lyrics",)


class Lyrics(BaseModel, frozen=True, validate_types=False):
    __endpoint__ = Base.LYRICS

    title: str
    """The title of the song."""
    artist: str
    """The artist of the song."""
    lyrics: str
    """The lyrics of the song."""
    url: str | None
    """The URL to more information about the song."""
    thumbnail: str | None
    """The URL to the thumbnail of the song."""

    def __str__(self) -> str:
        return self.lyrics
