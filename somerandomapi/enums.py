from __future__ import annotations

from enum import Enum

__all__ = (
    "Animal",
    "Animu",
    "BaseEnum",
    "CanvasBorder",
    "CanvasCrop",
    "CanvasFilter",
    "CanvasOverlay",
    "Fact",
    "Img",
    "ResultType",
    "TweetTheme",
    "WelcomeBackground",
    "WelcomeTextColor",
    "WelcomeType",
)


class BaseEnum(Enum):
    def __str__(self) -> str:
        return self.value if isinstance(self.value, str) else self.name


class Animu(BaseEnum):
    """Enum resprenting all possible actions for the animu endpoints."""

    HUG = "hug"
    PAT = "pat"
    NOM = "nom"
    CRY = "cry"
    KISS = "kiss"
    POKE = "poke"


class Animal(BaseEnum):
    """Enum representing all possible actions for the animal endpoints."""

    FOX = "fox"
    CAT = "cat"
    BIRD = "bird"
    PANDA = "panda"
    RACCOON = "raccoon"
    KOALA = "koala"
    KANGAROO = "kangaroo"
    WHALE = "whale"
    DOG = "dog"


class Img(BaseEnum):
    """Enum representing all possible actions for the img endpoints."""

    FOX = "fox"
    CAT = "cat"
    PANDA = "panda"
    RED_PANDA = "red_panda"
    PIKACHU = "pikachu"
    RACOON = "racoon"
    KOALA = "koala"
    KANGAROO = "kangaroo"
    WHALE = "whale"
    DOG = "dog"
    BIRD = "bird"


class Fact(BaseEnum):
    """Enum representing all possible actions for the fact endpoints."""

    CAT = "cat"
    FOX = "fox"
    PANDA = "panda"
    KOALA = "koala"
    KANGAROO = "kangaroo"
    RACCOON = "raccoon"
    GIRAFFE = "giraffe"
    WHALE = "whale"
    ELEPHANT = "elephant"
    DOG = "dog"
    BIRD = "bird"


class CanvasFilter(BaseEnum):
    """Enum representing all possible filters for the canvas filter endpoint."""

    BLUE = "blue"
    BLURPLE = "blurple"
    BLURPLE_2 = "blurple2"
    BRIGHTNESS = "brightness"
    COLOR = "color"
    GREEN = "green"
    GREYSCALE = "greyscale"
    INVERT = "invert"
    INVERT_GREYSCALE = "invertgreyscale"
    RED = "red"
    SEPIA = "sepia"
    THRESHOLD = "threshold"
    BLUR = "blur"
    PIXELATE = "pixelate"


class CanvasOverlay(BaseEnum):
    """Enum representing all possible overlays for the canvas overlay endpoint."""

    COMRADE = "comrade"
    GAY = "gay"
    GLASS = "glass"
    JAIL = "jail"
    PASSED = "passed"
    TRIGGERED = "triggered"
    WASTED = "wasted"


class CanvasBorder(BaseEnum):
    """Enum representing all possible borders for the canvas border endpoint."""

    TRANSGENDER = "transgender"
    PANSEXUAL = "pansexual"
    NONBINARY = "nonbinary"
    LGBT = "lgbt"
    LESBIAN = "lesbian"
    BISEXUAL = "bisexual"


class CanvasCrop(BaseEnum):
    """Enum representing all possible crops for the canvas crop endpoint."""

    HEART = "heart"
    CIRCLE = "circle"


class WelcomeType(BaseEnum):
    """Enum representing all possible types for the welcome cards."""

    JOIN = "join"
    LEAVE = "leave"


class WelcomeBackground(BaseEnum):
    """Enum representing all possible backgrounds for the welcome cards."""

    BLOBDAY = "blobday"
    BLOBNIGHT = "blobnight"
    GAMING1 = "gaming1"
    GAMING2 = "gaming2"
    GAMING3 = "gaming3"
    GAMING4 = "gaming4"
    NIGHT = "night"
    RAINBOW = "rainbow"
    RAINBOW_GRADIENT = "rainbowgradient"
    SPACE = "space"
    STARS = "stars"
    STARS2 = "stars2"
    SUNSET = "sunset"


class WelcomeTextColor(BaseEnum):
    """Enum representing all possible text colors for the welcome cards."""

    RED = "red"
    ORANGE = "orange"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"
    INDIGO = "indigo"
    PURPLE = "purple"
    PINK = "pink"
    BLACK = "black"
    WHITE = "white"


class TweetTheme(BaseEnum):
    """Enum representing all possible themes for the tweet endpoint."""

    LIGHT = "light"
    DIM = "dim"
    DARK = "dark"


class ResultType(BaseEnum):
    """Enum representing all possible result types for the search endpoint."""

    ENCODE = 0
    DECODE = 1
