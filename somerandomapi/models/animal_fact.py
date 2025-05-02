from .abc import BaseModel

__all__ = (
    "AnimalImageFact",
    "AnimalImageOrFact",
)


class AnimalImageFact(BaseModel, frozen=True, validate_types=False):
    """Represents an animal image

    This class is not meant to be instantiated by the user. Instead, get it through the
    :meth:`~somerandomapi.AnimalClient.get_image_and_fact` method on the :class:`~somerandomapi.AnimalClient`.
    """

    fact: str
    """The animal fact."""
    image: str
    """The animal image URL."""


class AnimalImageOrFact(BaseModel, frozen=True, validate_types=False):
    """Represents an animal image or fact.

    This class is not meant to be instantiated by the user. Instead, get it through the
    :meth:`~somerandomapi.AnimalClient.get_image_or_fact` method on the :class:`~somerandomapi.AnimalClient`.
    """

    fact: str | None
    """The animal fact if available."""
    image: str | None
    """The animal image URL if available."""
