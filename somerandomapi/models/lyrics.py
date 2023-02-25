from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ..internals.endpoints import Others as OthersEndpoint
from .abc import BaseModel


if TYPE_CHECKING:
    from ..types.others import LyricsLinks as LyricsLinksPayload

__all__ = ("Lyrics", "LyricsLinks")


@dataclass
class LyricsLinks(BaseModel):
    """Represents the links of a lyrics.

    This class is not meant to be instantiated by the user. Instead, access it through the `links` attribute of the `Client` class.
    """

    data: LyricsLinksPayload
    genius: str
    """The Genius link of the lyrics."""


@dataclass
class Lyrics(BaseModel):
    _endpoint = OthersEndpoint.LYRICS
    title: str
    """The title of the song."""
    author: str
    """The author of the song."""
    lyrics: str
    """The lyrics of the song."""

    _thumbnail: LyricsLinksPayload = field(repr=False)
    _links: LyricsLinksPayload = field(repr=False)

    if TYPE_CHECKING:

        @classmethod
        def from_dict(
            cls, *, title: str, author: str, lyrics: str, thumbnail: LyricsLinksPayload, links: LyricsLinksPayload
        ):
            ...

    @property
    def thumbnail(self) -> LyricsLinks:
        """The thumbnail of the lyrics."""
        return LyricsLinks(
            genius=self._thumbnail["genius"],
            data=self._thumbnail,
        )

    @property
    def links(self) -> LyricsLinks:
        """The links of the lyrics."""
        return LyricsLinks(
            genius=self._thumbnail["genius"],
            data=self._thumbnail,
        )
