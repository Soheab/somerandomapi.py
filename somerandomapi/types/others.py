from typing import TypedDict


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


class LyricsLinks(TypedDict):
    genius: str


class Lyrics(TypedDict):
    title: str
    author: str
    lyrics: str
    thumbnail: LyricsLinks
    links: LyricsLinks
