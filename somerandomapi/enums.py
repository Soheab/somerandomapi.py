from enum import Enum


__all__ = (
    "BaseEnum",
    "Animu",
    "Animal",
    "Img",
    "Fact",
    "CanvasFilter",
    "CanvasOverlay",
    "CanvasBorder",
    "CanvasCrop",
    "WelcomeType",
    "WelcomeBackground",
    "WelcomeTextColor",
    "TweetTheme",
    "ResultType",
)


class BaseEnum(Enum):
    def __str__(self) -> str:
        return self.value if isinstance(self.value, str) else self.name


class Animu(BaseEnum):
    HUG = "hug"
    PAT = "pat"
    NOM = "nom"
    CRY = "cry"
    KISS = "kiss"
    POKE = "poke"


class Animal(BaseEnum):
    """Enum holding all the animals that can be used in the animal endpoints."""

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
    COMRADE = "comrade"
    GAY = "gay"
    GLASS = "glass"
    JAIL = "jail"
    PASSED = "passed"
    TRIGGERED = "triggered"
    WASTED = "wasted"


class CanvasBorder(BaseEnum):
    TRANSGENDER = "transgender"
    PANSEXUAL = "pansexual"
    NONBINARY = "nonbinary"
    LGBT = "lgbt"
    LESBIAN = "lesbian"
    BISEXUAL = "bisexual"


class CanvasCrop(BaseEnum):
    HEART = "heart"
    CIRCLE = "circle"


class WelcomeType(BaseEnum):
    JOIN = "join"
    LEAVE = "leave"


class WelcomeBackground(BaseEnum):
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
    LIGHT = "light"
    DIM = "dim"
    DARK = "dark"


class ResultType(BaseEnum):
    ENCODE = 0
    DECODE = 1
