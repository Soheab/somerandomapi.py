from typing import Literal, TypedDict


Animals = Literal[
    "bird",
    "cat",
    "dog",
    "fox",
    "kangaroo",
    "koala",
    "panda",
    "raccoon",
    "red_panda",
]


class Animal(TypedDict):
    image: str
    fact: str
