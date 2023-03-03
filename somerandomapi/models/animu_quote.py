from dataclasses import dataclass


__all__ = ("AnimuQuote",)


@dataclass(frozen=True)
class AnimuQuote:
    """Represents an animu quote.

    This class is not meant to be instantiated by the user. Instead, access it through the :meth:`~somerandomapi.AnimuClient.quote` method of the :class:`~somerandomapi.AnimuClient` class.
    """

    sentence: str
    """The quote."""
    character: str
    """The character who said the quote."""
    anime: str
    """The anime the quote is from."""
