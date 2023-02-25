from typing import List, TypedDict


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
    pokemons: List[PokemonAbilityPokemons]
    descriptions: List[WithVersion]


class PokemonItem(WithNameIDAndEffects):
    cost: int
    attributes: List[str]
    category: str
    sprite: str
    descriptions: List[WithVersionAndDescription]


class PokemonMove(WithNameIDAndEffects):
    generation: int
    type: str
    category: str
    contest: str
    pp: int
    power: int
    accuracy: int
    pokemon: List[str]
    descriptions: List[WithVersionAndDescription]


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
    evolutionLine: List[str]


class PokeDexSprites(TypedDict):
    normal: str
    animated: str


class PokeDex(WithName):
    id: str
    type: List[str]
    species: List[str]
    abilities: List[str]
    height: str
    weight: str
    base_experience: str
    gender: List[str]
    egg_groups: List[str]
    stats: PokeDexStats
    family: PokeDexFamily
    sprites: PokeDexSprites
    description: str
    generation: str
