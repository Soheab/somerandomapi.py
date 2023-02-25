from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing_extensions import Self

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
    "PokemonAbility",
    "PokemonItem",
    "PokemonMove",
    "PokeDex",
)


class WithName:
    __slots__ = ("name",)

    def __init__(self, payload: WithNamePayload) -> None:
        self.name = payload["name"]


class WithNameID(WithName):
    __slots__ = ("id",)

    def __init__(self, payload: WithNameIDPayload) -> None:
        super().__init__(payload)
        self.id = payload["id"]


class WithNameIDAndEffects(WithNameID):
    __slots__ = ("effects",)

    def __init__(self, payload: WithNameIDAndEffectsPayload) -> None:
        super().__init__(payload)
        self.effects = payload["effects"]


class WithVersion:
    __slots__ = ("version",)

    def __init__(self, payload: WithVersionPayload) -> None:
        self.version = payload["version"]


class WithVersionAndDescription(WithVersion):
    __slots__ = ("description",)

    def __init__(self, payload: WithVersionAndDescriptionPayload) -> None:
        super().__init__(payload)
        self.description = payload["description"]


class PokemonAbilityPokemons:
    __slots__ = ("pokemon", "hidden")

    def __init__(self, payload: PokemonAbilityPokemonsPayload) -> None:
        self.pokemon = payload["pokemon"]
        self.hidden = payload["hidden"]


class PokemonAbility(WithNameIDAndEffects):
    __slots__ = ("generation", "description", "_data")

    def __init__(self, payload: PokemonAbilityPayload) -> None:
        super().__init__(payload)
        self._data: PokemonAbilityPayload = payload
        self.generation: int = payload["generation"]
        self.description: str = payload["description"]

    @classmethod
    def from_dict(cls, payload: PokemonAbilityPayload) -> Self:
        return cls(payload)

    @property
    def pokemons(self) -> list[PokemonAbilityPokemons]:
        return [PokemonAbilityPokemons(pokemon) for pokemon in self._data["pokemons"]]

    @property
    def descriptions(self) -> list[WithVersion]:
        return [WithVersion(description) for description in self._data["descriptions"]]


class PokemonItem(WithNameIDAndEffects):
    __slots__ = ("cost", "attributes", "category", "sprite", "_data")

    def __init__(self, payload: PokemonItemPayload) -> None:
        super().__init__(payload)
        self._data: PokemonItemPayload = payload
        self.attributes: list[str] = payload["attributes"]

        self.cost: int = payload["cost"]
        self.category: str = payload["category"]
        self.sprite: str = payload["sprite"]

    @classmethod
    def from_dict(cls, payload: PokemonItemPayload) -> Self:
        return cls(payload)

    @property
    def descriptions(self) -> list[WithVersionAndDescription]:
        return [WithVersionAndDescription(description) for description in self._data["descriptions"]]


class PokemonMove(WithNameIDAndEffects):
    __slots__ = (
        "generation",
        "type",
        "category",
        "contest",
        "pp",
        "power",
        "accuracy",
        "pokemon",
        "_data",
    )

    def __init__(self, payload: PokemonMovePayload) -> None:
        super().__init__(payload)
        self._data: PokemonMovePayload = payload
        self.pokemon: list[str] = payload["pokemon"]

        self.generation: int = payload["generation"]
        self.type: str = payload["type"]
        self.category: str = payload["category"]
        self.contest: str = payload["contest"]
        self.pp: int = payload["pp"]
        self.power: int = payload["power"]
        self.accuracy: int = payload["accuracy"]

    @classmethod
    def from_dict(cls, payload: PokemonMovePayload) -> Self:
        return cls(payload)

    @property
    def descriptions(self) -> list[WithVersionAndDescription]:
        return [WithVersionAndDescription(description) for description in self._data["descriptions"]]


class PokeDexStats:
    __slots__ = ("hp", "attack", "defense", "sp_atk", "sp_def", "speed", "total")

    def __init__(self, payload: PokeDexStatsPayload) -> None:
        self.hp: str = payload["hp"]
        self.attack: str = payload["attack"]
        self.defense: str = payload["defense"]
        self.sp_atk: str = payload["sp_atk"]
        self.sp_def: str = payload["sp_def"]
        self.speed: str = payload["speed"]
        self.total: str = payload["total"]


class PokeDexFamily:
    __slots__ = ("evolution_stage", "evolution_line")

    def __init__(self, payload: PokeDexFamilyPayload) -> None:
        self.evolution_line: list[str] = payload["evolutionLine"]

        self.evolution_stage: int = payload["evolutionStage"]


class PokeDexSprites:
    __slots__ = ("normal", "animated")

    def __init__(self, payload: PokeDexSpritesPayload) -> None:
        self.normal: str = payload["normal"]
        self.animated: str = payload["animated"]


class PokeDex(WithName):
    __slots__ = (
        "id",
        "type",
        "species",
        "abilities",
        "height",
        "base_experience",
        "gender",
        "egg_groups",
        "description",
        "generation",
        "_data",
    )

    def __init__(self, payload: PokeDexPayload) -> None:
        super().__init__(payload)
        self._data: PokeDexPayload = payload
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

    @classmethod
    def from_dict(cls, payload: PokeDexPayload) -> Self:
        return cls(payload)

    @property
    def family(self) -> PokeDexFamily:
        return PokeDexFamily(self._data["family"])

    @property
    def stats(self) -> PokeDexStats:
        return PokeDexStats(self._data["stats"])

    @property
    def sprites(self) -> PokeDexSprites:
        return PokeDexSprites(self._data["sprites"])
