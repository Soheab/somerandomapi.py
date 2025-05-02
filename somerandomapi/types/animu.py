from typing import Literal, TypedDict

from .http import WithLink

ValidAnimu = Literal[
    "nom",
    "poke",
    "cry",
    "kiss",
    "pat",
    "hug",
]


class Animu(WithLink):
    type: ValidAnimu


class AnimuQuote(TypedDict):
    quote: str
    anime: str
    id: int
    name: str
