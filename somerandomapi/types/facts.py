from typing import Literal, TypedDict


Animals = Literal[
    "bird",
    "cat",
    "dog",
    "fox",
    "koala",
    "panda",
]


class Fact(TypedDict):
    fact: str
