from typing import TYPE_CHECKING, Literal, TypedDict

from .http import WithLink


Animus = Literal[
    "facepalm",
    "hug",
    "pat",
    "wink",
    "quote",
]


class Animu(WithLink):
    ...


class AnimuQuote(TypedDict):
    sentance: str
    character: str
    anime: str
