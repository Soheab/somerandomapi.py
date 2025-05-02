from __future__ import annotations

from typing import TYPE_CHECKING

from somerandomapi.clients.animal import BaseClient

from ..internals.endpoints import Pokemon as PokemonEndpoints
from ..models.pokemon import PokeDex, PokemonAbility, PokemonItem, PokemonMove

__all__ = ("PokemonClient",)


class PokemonClient(BaseClient):
    """Represents the "Pokemon" endpoint.

    This class is not meant to be instantiated by the user. Instead, access it through the
    :attr:`~somerandomapi.Client.pokemon` attribute of the :class:`~somerandomapi.Client` class.
    """

    async def get_ability(self, ability: str) -> PokemonAbility:
        """Get a pokemon ability's information.

        Parameters
        ----------
        ability: :class:`str`
            The ability name or id of a pokemon ability.

        Returns
        -------
        :class:`PokemonAbility`
            Object representing the pokemon ability.
        """
        res = await self._http.request(PokemonEndpoints.ABILITIES, ability=ability)
        return PokemonAbility(res)

    async def get_item(self, item: str) -> PokemonItem:
        """Get a pokemon item's information.


        Parameters
        ----------
        item: :class:`str`
            The Item name or id of a pokemon item.

        Returns
        -------
        :class:`PokemonItem`
            Object representing the pokemon item.
        """
        res = await self._http.request(PokemonEndpoints.ITEMS, item=item)
        return PokemonItem(res)

    async def get_moves(self, move: str) -> PokemonMove:
        """Get a pokemon move's information.

        Parameters
        ----------
        move: :class:`str`
            The pokemon move name or id of a pokemon move

        Returns
        -------
        :class:`PokemonMove`
            Object representing the pokemon move.
        """
        res = await self._http.request(PokemonEndpoints.MOVES, move=move)
        return PokemonMove(res)

    async def get_pokedex(self, pokemon: str) -> PokeDex:
        """Get a pokemon's pokedex entry.

        Parameters
        ----------
        pokemon: :class:`str`
            The pokemon to get the pokedex entry for.

        Returns
        -------
        :class:`PokeDex`
            Object representing the pokedex entry.
        """
        res = await self._http.request(PokemonEndpoints.POKEDEX, pokemon=pokemon)
        return PokeDex(res)
