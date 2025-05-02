from typing import Literal, TypedDict

Filters = Literal[
    "blue",
    "blurple",
    "blurple2",
    "brightness",
    "color",
    "green",
    "greyscale",
    "invert",
    "invertgreyscale",
    "red",
    "sepia",
    "threshold",
    "blur",
    "pixelate",
]

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

Overlays = Literal[
    "comrade",
    "gay",
    "glass",
    "jail",
    "passed",
    "triggered",
    "wasted",
]


class HexOriginal(TypedDict):
    red: str
    green: str
    blue: str


class Hex(TypedDict):
    hex: str
    original: HexOriginal


class RGB(TypedDict):
    r: int
    g: int
    b: int
