from typing import Literal, TypedDict


Crops = Literal[
    "circle",
    "heart",
]
Borders = Literal[
    "lesbian",
    "nonbinary",
    "pansexual",
    "transgender",
    "lgbt",
]


class Hex(TypedDict):
    hex: str


class RGB(TypedDict):
    r: int
    g: int
    b: int
