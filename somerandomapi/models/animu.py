from typing import Self

from .abc import BaseModel

__all__ = ("AnimuQuote",)


class AnimuQuote(BaseModel, frozen=True, validate_types=False):
    """Represents an animu quote.

    This class is not meant to be instantiated by the user. Instead, access it through the
    :meth:`~somerandomapi.AnimuClient.random_quote` method of the :class:`~somerandomapi.AnimuClient` class.
    """

    quote: str
    """The quote."""
    anime: str
    """The anime the quote is from."""
    id: int
    """The ID of the quote."""
    name: str
    """The name of the character who said the quote."""

    @classmethod
    def from_dict(
        cls: type[Self],
        *,
        quote: str,
        anime: str,
        id: int,  # noqa: A002
        name: str,
    ) -> Self:
        return cls(quote=quote, anime=anime, id=id, name=name)
