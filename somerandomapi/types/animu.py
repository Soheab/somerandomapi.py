from typing import Literal, TypedDict

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
    sentence: str
    character: str
    anime: str
