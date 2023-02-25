from __future__ import annotations

from typing import TYPE_CHECKING

from ..internals.endpoints import Pokemon as PokemonEndpoints
from ..models.pokemon import PokeDex, PokemonAbility, PokemonItem, PokemonMove


if TYPE_CHECKING:
    from ..internals.http import HTTPClient


__all__ = ("Pokemon",)


class Pokemon:
    """Represents the "Pokemon" endpoint.

    This class is not meant to be instantiated by the user. Instead, access it through the `pokemon` attribute of the `Client` class.
    """

    __slots__ = ("__http",)

    def __init__(self, http: HTTPClient) -> None:
        self.__http: HTTPClient = http

    async def get_ability(self, ability: str) -> PokemonAbility:
        res = await self.__http.request(PokemonEndpoints.ABILITIES, ability=ability)
        return PokemonAbility(res)

    async def get_item(self, item: str) -> PokemonItem:
        res = await self.__http.request(PokemonEndpoints.ITEMS, item=item)
        return PokemonItem(res)

    async def get_moves(self, move: str) -> PokemonMove:
        res = await self.__http.request(PokemonEndpoints.MOVES, move=move)
        return PokemonMove(res)

    async def get_pokedex(self, pokemon: str) -> PokeDex:
        res = await self.__http.request(PokemonEndpoints.POKEDEX, pokemon=pokemon)
        return PokeDex(res)
