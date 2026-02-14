import asyncio
from types import SimpleNamespace

import pytest

from somerandomapi.clients.animal import AnimalClient
from somerandomapi.clients.animu import AnimuClient
from somerandomapi.clients.canvas import CanvasClient
from somerandomapi.clients.chatbot import Chatbot
from somerandomapi.clients.client import Client
from somerandomapi.clients.pokemon import PokemonClient
from somerandomapi.clients.premium import PremiumClient
from somerandomapi.enums import (
    Animu as AnimuEnum,
    CanvasFilter,
    CanvasOverlay,
    Fact,
    Img,
    TweetTheme,
    WelcomeBackground,
    WelcomeTextColor,
    WelcomeType,
)
from somerandomapi.internals.endpoints import Base as BaseEndpoint
from somerandomapi.models.image import Image
from somerandomapi.models.namecard import GenshinNamecard
from somerandomapi.models.rankcard import Rankcard
from somerandomapi.models.tweet import Tweet
from somerandomapi.models.welcome.free import WelcomeFree
from somerandomapi.models.youtube_comment import YoutubeComment


def _run(coro):
    async def _await_any(awaitable):
        return await awaitable

    return asyncio.run(_await_any(coro))


class DummyHTTP:
    def __init__(self):
        self.calls = []
        self.closed = False

    async def request(self, endpoint, **kwargs):
        path = endpoint.path if hasattr(endpoint, "path") else endpoint.value.path
        self.calls.append((path, kwargs))
        if path.endswith("base64"):
            return {"encoded": "aGk=", "decoded": "hi"}
        if path.endswith("binary"):
            return {"encoded": "1101000 1101001", "decoded": "hi"}
        if path.endswith("quote"):
            return {"quote": "q", "anime": "a", "id": 1, "name": "n"}
        if "chatbot" in path:
            return {"response": "hello"}
        if "lyrics" in path:
            return {"title": "t", "artist": "a", "lyrics": "l", "url": "u", "thumbnail": "th"}
        if "joke" in path:
            return {"joke": "j"}
        if "bottoken" in path:
            return {"token": "tok"}
        if "hex" in path and "canvas/hex" in path:
            return {"hex": "ffffff", "original": {"red": "255", "green": "255", "blue": "255"}}
        if path.endswith("rgb"):
            return {"r": 1, "g": 2, "b": 3}
        if "pokemon/abilities" in path:
            return {
                "name": "x",
                "id": 1,
                "effects": "e",
                "generation": 1,
                "description": "d",
                "pokemons": [{"pokemon": "p", "hidden": False}],
                "descriptions": [{"version": "v"}],
            }
        if "pokemon/items" in path:
            return {
                "name": "x",
                "id": 1,
                "effects": "e",
                "cost": 1,
                "attributes": ["a"],
                "category": "c",
                "sprite": "s",
                "descriptions": [{"version": "v", "description": "d"}],
            }
        if "pokemon/moves" in path:
            return {
                "name": "x",
                "id": 1,
                "effects": "e",
                "generation": 1,
                "type": "fire",
                "category": "special",
                "contest": "cool",
                "pp": 10,
                "power": 50,
                "accuracy": 100,
                "pokemon": ["a"],
                "descriptions": [{"version": "v", "description": "d"}],
            }
        if "pokemon/pokedex" in path:
            return {
                "name": "pikachu",
                "id": "25",
                "type": ["electric"],
                "species": ["mouse"],
                "abilities": ["static"],
                "height": "4",
                "base_experience": "112",
                "gender": ["male", "female"],
                "egg_groups": ["field"],
                "stats": {
                    "hp": "35",
                    "attack": "55",
                    "defense": "40",
                    "sp_atk": "50",
                    "sp_def": "50",
                    "speed": "90",
                    "total": "320",
                },
                "family": {"evolutionStage": 2, "evolutionLine": ["pichu", "pikachu"]},
                "sprites": {"normal": "n", "animated": "a"},
                "description": "desc",
                "generation": "1",
            }
        if "facts" in path:
            return {"fact": "f"}
        if "img/" in path or "animu/" in path:
            return {"link": "https://img"}
        if "animal/" in path:
            return {"fact": "f", "image": "https://img"}
        if "canvas/" in path or "premium/" in path:
            return Image.construct("https://generated", self)
        return {"ok": True}

    async def close(self):
        self.closed = True


def test_animu_client() -> None:
    http = DummyHTTP()
    client = AnimuClient(http)
    assert _run(client.get(AnimuEnum.HUG)) == "https://img"
    assert _run(client.hug()) == "https://img"
    quote = _run(client.random_quote())
    assert quote.quote == "q"


def test_animal_client() -> None:
    http = DummyHTTP()
    client = AnimalClient(http)
    both = _run(client.get_image_and_fact("fox"))
    assert both.fact == "f"
    assert _run(client.get_image(Img.FOX)) == "https://img"
    assert _run(client.get_fact(Fact.FOX)) == "f"
    partial = _run(client.get_image_or_fact("fox"))
    assert partial.fact or partial.image


def test_canvas_client_and_memes() -> None:
    http = DummyHTTP()
    client = CanvasClient(http)
    assert isinstance(_run(client.filter("https://a", CanvasFilter.BLUE)), Image)
    assert isinstance(_run(client.blue_filter("https://a")), Image)
    assert isinstance(_run(client.overlay("https://a", CanvasOverlay.GAY)), Image)
    assert isinstance(_run(client.color_viewer("#ffffff")), Image)

    with pytest.raises(TypeError):
        _run(client.generate_tweet(display_name="d", username="u", avatar_url="https://a", text="t", theme=TweetTheme.LIGHT))
    with pytest.raises(TypeError):
        _run(client.generate_youtube_comment(avatar_url="https://a", username="u", text="c"))
    with pytest.raises(TypeError):
        _run(client.generate_genshin_namecard(avatar_url="https://a", birthday="01/01/2000", username="u"))

    assert isinstance(_run(client.memes.oogway("hi")), Image)
    assert isinstance(_run(client.memes.no_bitches(avatar_url="https://a", no="no")), Image)


def test_pokemon_client() -> None:
    http = DummyHTTP()
    client = PokemonClient(http)
    assert _run(client.get_ability("static")).name == "x"
    assert _run(client.get_item("item")).name == "x"
    assert _run(client.get_moves("move")).name == "x"
    assert _run(client.get_pokedex("pikachu")).name == "pikachu"


def test_premium_client() -> None:
    http = DummyHTTP()
    client = PremiumClient(http)
    assert isinstance(_run(client.amongus("https://a", "u")), Image)
    assert isinstance(_run(client.petpet("https://a")), Image)

    with pytest.raises(TypeError):
        _run(client.rankcard(template=1, username="u", avatar_url="https://a", level=1, current_xp=1, needed_xp=2))

    with pytest.raises(TypeError):
        _run(
            client.welcome_image(
                template=1,
                type=WelcomeType.JOIN,
                username="u",
                avatar_url="https://a",
                discriminator=1,
                server_name="s",
                member_count=1,
                text_color=WelcomeTextColor.WHITE,
                background_url="https://bg",
            )
        )


def test_chatbot_standalone_and_context() -> None:
    dummy = DummyHTTP()
    bot = Chatbot(message="hello", client=SimpleNamespace(_http=dummy))
    result = _run(bot.send("hello"))
    assert result.response == "hello"


def test_top_level_client_features() -> None:
    c = Client()
    dummy = DummyHTTP()
    c._http = dummy
    assert _run(c.encode_base64("hi")).name == "BASE64"
    assert _run(c.decode_binary("10")).name == "BINARY"
    assert _run(c.generate_bot_token()) == "tok"
    assert _run(c.random_joke()) == "j"
    assert _run(c.lyrics("song")).title == "t"
    assert _run(c.rgb_to_hex("1,2,3")) == "ffffff"
    assert _run(c.hex_to_rgb("ffffff")).r == 1
    with pytest.raises(TypeError):
        _run(
            c.welcome_image(
                WelcomeFree(
                    template=1,
                    type=WelcomeType.JOIN,
                    background=WelcomeBackground.SPACE,
                    avatar_url="https://a",
                    username="u",
                    server_name="s",
                    member_count=1,
                    text_color=WelcomeTextColor.WHITE,
                )
            )
        )
    _run(c.close())
    assert any(path == BaseEndpoint.WELCOME.path for path, _ in dummy.calls)
