from typing import Literal, TypedDict

ValidFact = Literal[
    "cat",
    "fox",
    "panda",
    "koala",
    "kangaroo",
    "racoon",
    "giraffe",
    "whale",
    "elephant",
    "dog",
    "bird",
]


class Fact(TypedDict):
    fact: str
