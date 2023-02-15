from typing import Tuple

from dataclasses import dataclass

__all__: Tuple[str, ...] = ("AnimuQuote",)


@dataclass(frozen=True)
class AnimuQuote:
    """Represents an animu quote.

    This class is not meant to be instantiated by the user. Instead, access it through the `quote` method of the `Animu` class.

    Attributes
    ----------
    sentance: :class:`str`
        The quote.
    character: :class:`str`
        The character who said the quote.
    anime: :class:`str`
        The anime the quote is from.
    """

    sentance: str
    character: str
    anime: str
