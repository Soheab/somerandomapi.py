from dataclasses import dataclass
from typing import Optional


__all__ = ("AnimalImageFact", "AnimalImageOrFact")


@dataclass(frozen=True)
class AnimalImageFact:
    """Represents an animal image fact.

    This class is not meant to be instantiated by the user. Instead, get it through the :meth:`~somerandomapi.AnimalClient.get_image_and_fact` method on the :class:`~somerandomapi.AnimalClient`.
    """

    fact: str
    """The animal fact."""
    image: str
    """The animal image URL."""


@dataclass(frozen=True)
class AnimalImageOrFact:
    """Represents an animal image or fact.

    This class is not meant to be instantiated by the user. Instead, get it through the :meth:`~somerandomapi.AnimalClient.get_image_or_fact` method on the :class:`~somerandomapi.AnimalClient`.
    """

    fact: Optional[str]
    """The animal fact if available."""
    image: Optional[str]
    """The animal image URL if available."""
