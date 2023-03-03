from enum import Enum


__all__ = (
    "Animal",
    "ImgAnimal",
    "FactAnimal",
    "CanvasFilter",
    "CanvasOverlay",
    "CanvasBorder",
    "CanvasCrop",
    "WelcomeType",
    "WelcomeBackground",
    "WelcomeTextColor",
    "ResultType",
)


class BaseEnum(Enum):
    def __str__(self) -> str:
        return self.value if isinstance(self.value, str) else self.name


class Animal(BaseEnum):
    """Enum holding all the animals that can be used in the animal endpoints."""

    BIRD = "bird"
    CAT = "cat"
    DOG = "dog"
    FOX = "fox"
    KANGAROO = "kangaroo"
    KOALA = "koala"
    PANDA = "panda"
    RACCOON = "raccoon"
    RED_PANDA = "red_panda"


class ImgAnimal(BaseEnum):
    # Can't subclass Animal because of how enums work
    BIRD = "bird"
    CAT = "cat"
    DOG = "dog"
    FOX = "fox"
    KANGAROO = "kangaroo"
    KOALA = "koala"
    PANDA = "panda"
    RACCOON = "raccoon"
    RED_PANDA = "red_panda"
    ## ---------------------
    PIKACHU = "pikachu"
    WHALE = "whale"


class FactAnimal(BaseEnum):
    BIRD = "bird"
    CAT = "cat"
    DOG = "dog"
    FOX = "fox"
    KOALA = "koala"
    PANDA = "panda"


class CanvasFilter(BaseEnum):
    BLURPLE = "blurple"
    BLURPLE_2 = "blurple2"
    BRIGHTNESS = "brightness"
    COLOR = "color"
    BLUE = "blue"
    GREEN = "green"
    RED = "red"
    SEPIA = "sepia"
    GREYSCALE = "greyscale"
    INVERT = "invert"
    INVERT_GREYSCALE = "invertgreyscale"
    THRESHOLD = "threshold"

    # from misc but idk why they aren't part of filters
    BLUR = "blur"
    PIXELATE = "pixelate"
    JPG = "jpg"


class CanvasOverlay(BaseEnum):
    COMRADE = "comrade"
    GAY = "gay"
    GLASS = "glass"
    JAIL = "jail"
    TRIGGERED = "triggered"
    WASTED = "wasted"


class CanvasBorder(BaseEnum):
    LESBIAN = "lesbian"
    NONBINARY = "nonbinary"
    PANSEXUAL = "pansexual"
    TRANSGENDER = "transgender"

    # lgbt
    LGBT = "lgbt"
    # alises
    LGBTQPLUS = LGBT
    LGBTQ2SPLUS = LGBT


class CanvasCrop(BaseEnum):
    HEART = "heart"
    CIRCLE = "circle"


class WelcomeType(BaseEnum):
    JOIN = "join"
    LEAVE = "leave"


class WelcomeBackground(BaseEnum):
    STARS = "stars"
    STARS2 = "stars2"
    RAINBOW_GRADIENT = "rainbowgradient"
    RAINBOW = "rainbow"
    SUNSET = "sunset"
    NIGHT = "night"
    BLOBDAY = "blobday"
    BLOBNIGHT = "blobnight"
    SPACE = "space"
    GAMING1 = "gaming1"
    GAMING2 = "gaming2"
    GAMING3 = "gaming3"
    GAMING4 = "gaming4"


class WelcomeTextColor(BaseEnum):
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


class ResultType(BaseEnum):
    ENCODE = 0
    DECODE = 1
