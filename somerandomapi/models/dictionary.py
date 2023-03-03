from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..internals.endpoints import Others as OthersEndpoint
from .abc import BaseModel


__all__ = ("Dictionary",)


@dataclass
class Dictionary(BaseModel):
    _endpoint = OthersEndpoint.DICTIONARY
    """Represents a dictonary."""

    word: str
    """The word of the dictionary."""
    definition: str
    """The definition of the word."""

    if TYPE_CHECKING:

        @classmethod
        def from_dict(
            cls,
            *,
            word: str,
            definition: str,
        ) -> "Dictionary":
            ...
