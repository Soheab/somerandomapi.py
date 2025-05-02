from typing import Literal

from .http import WithLink

ValidImg = Literal[
    "fox",
    "cat",
    "panda",
    "red_panda",
    "pikachu",
    "racoon",
    "koala",
    "kangaroo",
    "whale",
    "dog",
    "bird",
]


class Img(WithLink): ...
