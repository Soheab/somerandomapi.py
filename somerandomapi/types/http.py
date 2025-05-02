from typing import Literal, TypedDict

WelcomeBackgrounds = Literal[
    "stars",
    "stars2",
    "rainbowgradient",
    "rainbow",
    "sunset",
    "night",
    "blobday",
    "blobnight",
    "space",
    "gaming1",
    "gaming2",
    "gaming3",
    "gaming4",
]
WelcomeTextColors = Literal["red", "orange", "yellow", "green", "blue", "indigo", "purple", "pink", "black", "white"]


class WithLink(TypedDict):
    link: str


class WithText(TypedDict):
    text: str


class Base64(WithText):
    base64: str


class Binary(WithText):
    binary: str


class BotToken(TypedDict):
    token: str


class Dictionary(TypedDict):
    word: str
    definition: str


class Joke(TypedDict):
    joke: str


class Lyrics(TypedDict):
    title: str
    artist: str
    lyrics: str
    url: str
    thumbnail: str


class Chatbot(TypedDict):
    response: str
