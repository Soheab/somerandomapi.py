from somerandomapi import Client
from somerandomapi.clients import AnimalClient, AnimuClient, CanvasClient, Chatbot, PokemonClient, PremiumClient
from somerandomapi.models import (
    RGB,
    AnimalImageFact,
    AnimalImageOrFact,
    AnimuQuote,
    ChatbotResult,
    EncodeResult,
    GenshinNamecard,
    Image,
    Lyrics,
    PokeDex,
    Rankcard,
    Tweet,
    WelcomeFree,
    WelcomePremium,
    YoutubeComment,
)


def test_public_imports_are_available() -> None:
    assert Client is not None
    assert AnimalClient is not None
    assert AnimuClient is not None
    assert CanvasClient is not None
    assert Chatbot is not None
    assert PokemonClient is not None
    assert PremiumClient is not None

    assert AnimalImageFact is not None
    assert AnimalImageOrFact is not None
    assert AnimuQuote is not None
    assert ChatbotResult is not None
    assert EncodeResult is not None
    assert GenshinNamecard is not None
    assert Image is not None
    assert Lyrics is not None
    assert PokeDex is not None
    assert Rankcard is not None
    assert RGB is not None
    assert Tweet is not None
    assert WelcomeFree is not None
    assert WelcomePremium is not None
    assert YoutubeComment is not None
