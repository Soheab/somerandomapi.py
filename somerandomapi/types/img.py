from typing import Literal

from .http import WithLink


Images = Literal[
    "bird",
    "cat",
    "dog",
    "fox",
    "kangaroo",
    "koala",
    "panda",
    "raccoon",
    "pikachu",
    "red_panda",
    "whale",
]


class Img(WithLink):
    ...
