from dataclasses import dataclass


__all__ = ("AnimalImageFact",)


@dataclass(frozen=True)
class AnimalImageFact:
    """Represents an animal image fact.

    This class is not meant to be instantiated by the user. Instead, get it through the :meth:`~somerandomapi.AnimalClient.get_image_and_fact` method on the :class:`~somerandomapi.AnimalClient`.
    """

    fact: str
    """The animal fact."""
    image: str
    """The animal image URL."""
