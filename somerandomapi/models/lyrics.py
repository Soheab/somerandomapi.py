from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

from ..internals.endpoints import Others as OthersEndpoint
from .abc import BaseModel


__all__ = ("Lyrics", "LyricsLinks")


class LyricsLinks:
    """Represents the links of a lyrics.

    This class is not meant to be instantiated by the user. Instead, access it through the :attr:`Lyrics.links` attribute of the :class:`.clients.client.Client` class.

    Attributes
    ----------
    genius: :class:`str`
        The genius link.
    """

    def __init__(self, data: dict[str, Any]) -> None:
        self.data: dict[str, Any] = data
        self.genius: str = data["genius"]


@dataclass
class Lyrics(BaseModel):
    _endpoint = OthersEndpoint.LYRICS
    title: str
    """The title of the song."""
    author: str
    """The author of the song."""
    lyrics: str
    """The lyrics of the song."""

    _thumbnail: dict[str, Any] = field(repr=False)
    _links: dict[str, Any] = field(repr=False)

    if TYPE_CHECKING:

        @classmethod
        def from_dict(
            cls, *, title: str, author: str, lyrics: str, thumbnail: dict[str, Any], links: dict[str, Any]
        ) -> "Lyrics":
            ...

    @property
    def thumbnail(self) -> LyricsLinks:
        """The thumbnail of the lyrics."""
        return LyricsLinks(
            data=self._thumbnail,
        )

    @property
    def links(self) -> LyricsLinks:
        """The links of the lyrics."""
        return LyricsLinks(
            data=self._thumbnail,
        )
