from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

from dataclasses import dataclass

from .abc import BaseModel

if TYPE_CHECKING:
    from typing_extensions import Unpack

    from ..types.others import Lyrics as LyricsPayload, LyricsLinks as LyricsLinksPayload

__all__: Tuple[str, ...] = ("Lyrics", "LyricsLinks")


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
    title: str
    """The title of the song."""
    author: str
    """The author of the song."""

    _thumbnail: LyricsLinksPayload
    _links: LyricsLinksPayload

    if TYPE_CHECKING:

        @classmethod
        def from_dict(cls, **data: Unpack[LyricsPayload]):
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
