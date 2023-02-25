from dataclasses import dataclass


__all__ = ("AnimalImageFact",)


@dataclass(frozen=True)
class AnimalImageFact:
    """Represents an animal image fact.

    This class is not meant to be instantiated by the user. Instead, access it through the `image_fact` method of the `Animal` class.

    Attributes
    ----------
    fact: :class:`str`
        The fact.
    image: :class:`str`
        The image URL.
    """

    fact: str
    image: str
