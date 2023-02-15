from typing import TYPE_CHECKING, Tuple

from dataclasses import dataclass
from .abc import BaseModel

__all__: Tuple[str, ...] = ("Dictionary",)


@dataclass()
class Dictionary(BaseModel):
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
        ):
            ...
