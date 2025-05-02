from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..types.pokemon import (
        PokeDex as PokeDexPayload,
        PokeDexFamily as PokeDexFamilyPayload,
        PokeDexSprites as PokeDexSpritesPayload,
        PokeDexStats as PokeDexStatsPayload,
        PokemonAbility as PokemonAbilityPayload,
        PokemonAbilityPokemons as PokemonAbilityPokemonsPayload,
        PokemonItem as PokemonItemPayload,
        PokemonMove as PokemonMovePayload,
        WithName as WithNamePayload,
        WithNameID as WithNameIDPayload,
        WithNameIDAndEffects as WithNameIDAndEffectsPayload,
        WithVersion as WithVersionPayload,
        WithVersionAndDescription as WithVersionAndDescriptionPayload,
    )

__all__ = (
    "PokeDex",
    "PokeDexFamily",
    "PokeDexSprites",
    "PokeDexStats",
    "PokemonAbility",
    "PokemonAbilityPokemons",
    "PokemonItem",
    "PokemonMove",
    "WithName",
    "WithNameID",
    "WithNameIDAndEffects",
    "WithVersion",
    "WithVersionAndDescription",
)


class WithName:
    __slots__ = ("name",)

    def __init__(self, payload: WithNamePayload) -> None:
        self.name = payload["name"]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name}>"


class WithNameID(WithName):
    __slots__ = ("id",)

    def __init__(self, payload: WithNameIDPayload) -> None:
        super().__init__(payload)
        self.id: int = payload["id"]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} id={self.id!r}>"


class WithNameIDAndEffects(WithNameID):
    __slots__ = ("effects",)

    def __init__(self, payload: WithNameIDAndEffectsPayload) -> None:
        super().__init__(payload)
        self.effects: str = payload["effects"]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} id={self.id!r} effects={self.effects!r}>"


class WithVersion:
    __slots__ = ("version",)

    def __init__(self, payload: WithVersionPayload) -> None:
        self.version: str = payload["version"]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} version={self.version!r}>"


class WithVersionAndDescription(WithVersion):
    __slots__ = ("description",)

    def __init__(self, payload: WithVersionAndDescriptionPayload) -> None:
        super().__init__(payload)
        self.description: str = payload["description"]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} version={self.version!r} description={self.description!r}>"


class PokemonAbilityPokemons:
    """Represents a Pokemon's ability.

    Attributes
    ----------
    pokemon: :class:`str`
        The name of the Pokemon.
    hidden: :class:`bool`
        Whether the ability is hidden or not.
    """

    __slots__ = ("hidden", "pokemon")

    def __init__(self, payload: PokemonAbilityPokemonsPayload) -> None:
        self.pokemon: str = payload["pokemon"]
        self.hidden: bool = payload["hidden"]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} pokemon={self.pokemon!r} hidden={self.hidden!r}>"


class PokemonAbility(WithNameIDAndEffects):
    """Represents a Pokemon's ability.

    Attributes
    ----------
    name: :class:`str`
        The name of the ability.
    id: :class:`int`
        The ID of the ability.
    effects: :class:`str`
        The effects of the ability.
    generation: :class:`int`
        The generation of the ability.
    description: :class:`str`
        The description of the ability.
    """

    __slots__ = ("_descriptions", "_pokemons", "description", "generation")

    def __init__(self, payload: PokemonAbilityPayload) -> None:
        super().__init__(payload)
        self._descriptions = [WithVersion(description) for description in payload["descriptions"]]
        self._pokemons = [PokemonAbilityPokemons(pokemon) for pokemon in payload["pokemons"]]

        self.generation = payload["generation"]
        self.description = payload["description"]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} id={self.id!r} generation={self.generation!r}>"

    @property
    def pokemons(self) -> list[PokemonAbilityPokemons]:
        """List[:class:`.PokemonAbilityPokemons`]: A list of Pokemon's that have this ability."""
        return self._pokemons

    @property
    def descriptions(self) -> list[WithVersion]:
        """A list of descriptions with their version.

        Returns
        -------
        An object with the following attributes:
        - ``version``: :class:`str`
            The version of the description.
        """
        return self._descriptions


class PokemonItem(WithNameIDAndEffects):
    """Represents a Pokemon's item.

    Attributes
    ----------
    name: :class:`str`
        The name of the item.
    id: :class:`int`
        The ID of the item.
    effects: :class:`str`
        The effects of the item.
    cost: :class:`int`
        The cost of the item.
    category: :class:`str`
        The category of the item.
    sprite: :class:`str`
        The sprite of the item.
    """

    __slots__ = ("_descriptions", "attributes", "category", "cost", "sprite")

    def __init__(self, payload: PokemonItemPayload) -> None:
        super().__init__(payload)
        self._descriptions: list[WithVersionAndDescription] = [
            WithVersionAndDescription(description) for description in payload["descriptions"]
        ]

        self.attributes: list[str] = payload["attributes"]
        self.cost: int = payload["cost"]
        self.category: str = payload["category"]
        self.sprite: str = payload["sprite"]

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} name={self.name!r} id={self.id!r} "
            f"cost={self.cost!r} category={self.category!r} sprite={self.sprite!r}>"
        )

    @property
    def descriptions(self) -> list[WithVersionAndDescription]:
        """A list of descriptions with their version.

        Returns
        -------
        An object with the following attributes:
        - ``version``: :class:`str`
            The version of the description.
        - ``description``: :class:`str`
            The description of the item.
        """
        return self._descriptions


class PokemonMove(WithNameIDAndEffects):
    """Represents a Pokemon's move.

    Attributes
    ----------
    name: :class:`str`
        The name of the move.
    id: :class:`int`
        The ID of the move.
    effects: :class:`str`
        The effects of the move.
    generation: :class:`int`
        The generation of the move.
    type: :class:`str`
        The type of the move.
    category: :class:`str`
        The category of the move.
    contest: :class:`str`
        The contest of the move.
    pp: :class:`int`
        The PP of the move.
    power: :class:`int`
        The power of the move.
    accuracy: :class:`int`
        The accuracy of the move.
    pokemon: List[:class:`str`]
        A list of Pokemon's that have this move.
    """

    __slots__ = (
        "_descriptions",
        "accuracy",
        "category",
        "contest",
        "generation",
        "pokemon",
        "power",
        "pp",
        "type",
    )

    def __init__(self, payload: PokemonMovePayload) -> None:
        super().__init__(payload)
        self._descriptions: list[WithVersionAndDescription] = [
            WithVersionAndDescription(description) for description in payload["descriptions"]
        ]

        self.pokemon: list[str] = payload["pokemon"]
        self.generation: int = payload["generation"]
        self.type: str = payload["type"]
        self.category: str = payload["category"]
        self.contest: str = payload["contest"]
        self.pp: int = payload["pp"]
        self.power: int = payload["power"]
        self.accuracy: int = payload["accuracy"]

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} name={self.name!r} id={self.id!r} "
            f"generation={self.generation!r} type={self.type!r} category={self.category!r}>"
        )

    @property
    def descriptions(self) -> list[WithVersionAndDescription]:
        """A list of descriptions with their version.

        Returns
        -------
        An object with the following attributes:
        - ``version``: :class:`str`
            The version of the description.
        - ``description``: :class:`str`
            The description of the move.
        """
        return self._descriptions


class PokeDexStats:
    """Represents a Pokemon's stats.

    Attributes
    ----------
    hp: :class:`str`
        The HP of the Pokemon.
    attack: :class:`str`
        The attack of the Pokemon.
    defense: :class:`str`
        The defense of the Pokemon.
    special_attack: :class:`str`
        The special attack of the Pokemon.
    special_defence: :class:`str`
        The special defence of the Pokemon.
    speed: :class:`str`
        The speed of the Pokemon.
    total: :class:`str`
        The total of the Pokemon.
    """

    __slots__ = ("attack", "defense", "hp", "special_attack", "special_defence", "speed", "total")

    def __init__(self, payload: PokeDexStatsPayload) -> None:
        self.hp: str = payload["hp"]
        self.attack: str = payload["attack"]
        self.defense: str = payload["defense"]
        self.special_attack: str = payload["sp_atk"]
        self.special_defence: str = payload["sp_def"]
        self.speed: str = payload["speed"]
        self.total: str = payload["total"]

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} hp={self.hp!r} attack={self.attack!r} "
            f"defense={self.defense!r} special_attack={self.special_attack!r} "
            f"special_defence={self.special_defence!r} speed={self.speed!r} total={self.total!r}>"
        )


class PokeDexFamily:
    """Represents a Pokemon's family.

    Attributes
    ----------
    evolution_stage: :class:`int`
        The evolution stage of the Pokemon.
    evolution_line: List[:class:`str`]
        A list of the Pokemon's evolution line.
    """

    __slots__ = ("evolution_line", "evolution_stage")

    def __init__(self, payload: PokeDexFamilyPayload) -> None:
        self.evolution_line: list[str] = payload["evolutionLine"]
        self.evolution_stage: int = payload["evolutionStage"]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} evolution_stage={self.evolution_stage!r} evolution_line={self.evolution_line!r}>"


class PokeDexSprites:
    """Represents a Pokemon's sprites.

    Attributes
    ----------
    normal: :class:`str`
        The normal sprite of the Pokemon.
    animated: :class:`str`
        The animated sprite of the Pokemon.
    """

    __slots__ = ("animated", "normal")

    def __init__(self, payload: PokeDexSpritesPayload) -> None:
        self.normal: str = payload["normal"]
        self.animated: str = payload["animated"]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} normal={self.normal!r} animated={self.animated!r}>"


class PokeDex(WithName):
    """Represents a Pokedex

    name: :class:`str`
        The name of the Pokemon.
    id: :class:`str`
        The id of the Pokemon.
    type: List[:class:`str`]
        A list of the Pokemon's types.
    species: List[:class:`str`]
        A list of the Pokemon's species.
    abilities: List[:class:`str`]
        A list of the Pokemon's abilities.
    height: :class:`str`
        The height of the Pokemon.
    base_experience: :class:`str`
        The base experience of the Pokemon.
    gender: List[:class:`str`]
        List of genders for the Pokemon.
    egg_groups: List[:class:`str`]
        List of egg groups for the Pokemon.
    description: :class:`str`
        The description of the Pokemon.
    generation: :class:`str`
        The generation of the Pokemon.
    """

    __slots__ = (
        "_family",
        "_sprites",
        "_stats",
        "abilities",
        "base_experience",
        "description",
        "egg_groups",
        "gender",
        "generation",
        "height",
        "id",
        "species",
        "type",
    )

    def __init__(self, payload: PokeDexPayload) -> None:
        super().__init__(payload)
        self._family: PokeDexFamily = PokeDexFamily(payload["family"])
        self._stats: PokeDexStats = PokeDexStats(payload["stats"])
        self._sprites: PokeDexSprites = PokeDexSprites(payload["sprites"])

        self.type: list[str] = payload["type"]
        self.species: list[str] = payload["species"]
        self.abilities: list[str] = payload["abilities"]
        self.gender: list[str] = payload["gender"]
        self.egg_groups: list[str] = payload["egg_groups"]
        self.id: str = payload["id"]
        self.height: str = payload["height"]
        self.description: str = payload["description"]
        self.base_experience: str = payload["base_experience"]
        self.generation: str = payload["generation"]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id!r} name={self.name!r} description={self.description!r}>"

    @property
    def family(self) -> PokeDexFamily:
        """:class:`.PokeDexFamily`: The family of the Pokemon."""
        return self._family

    @property
    def stats(self) -> PokeDexStats:
        """:class:`.PokeDexStats`: The stats of the Pokemon."""
        return self._stats

    @property
    def sprites(self) -> PokeDexSprites:
        """:class:`.PokeDexSprites`: The sprites of the Pokemon."""
        return self._sprites
