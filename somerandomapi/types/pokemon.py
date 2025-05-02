from typing import TypedDict


class WithName(TypedDict):
    name: str


class WithNameID(WithName):
    id: int


class WithNameIDAndEffects(WithNameID):
    effects: str


class WithVersion(TypedDict):
    version: str


class WithVersionAndDescription(WithVersion):
    description: str


class PokemonAbilityPokemons(TypedDict):
    pokemon: str
    hidden: bool


class PokemonAbility(WithNameIDAndEffects):
    generation: int
    description: str
    pokemons: list[PokemonAbilityPokemons]
    descriptions: list[WithVersion]


class PokemonItem(WithNameIDAndEffects):
    cost: int
    attributes: list[str]
    category: str
    sprite: str
    descriptions: list[WithVersionAndDescription]


class PokemonMove(WithNameIDAndEffects):
    generation: int
    type: str
    category: str
    contest: str
    pp: int
    power: int
    accuracy: int
    pokemon: list[str]
    descriptions: list[WithVersionAndDescription]


class PokeDexStats(TypedDict):
    hp: str
    attack: str
    defense: str
    sp_atk: str
    sp_def: str
    speed: str
    total: str


class PokeDexFamily(TypedDict):
    evolutionStage: int
    evolutionLine: list[str]


class PokeDexSprites(TypedDict):
    normal: str
    animated: str


class PokeDex(WithName):
    id: str
    type: list[str]
    species: list[str]
    abilities: list[str]
    height: str
    weight: str
    base_experience: str
    gender: list[str]
    egg_groups: list[str]
    stats: PokeDexStats
    family: PokeDexFamily
    sprites: PokeDexSprites
    description: str
    generation: str
