from typing import Literal, TypedDict

ValidAnimal = Literal[
    "fox",
    "cat",
    "panda",
    "racoon",
    "koala",
    "kangaroo",
    "whale",
    "dog",
    "bird",
]


class Animal(TypedDict):
    image: str
    fact: str
