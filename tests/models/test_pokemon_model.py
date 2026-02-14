from somerandomapi.models.pokemon import PokeDex, PokemonAbility, PokemonItem, PokemonMove


def test_pokemon_ability_model() -> None:
    payload = {
        "name": "static",
        "id": 1,
        "effects": "may paralyze",
        "generation": 1,
        "description": "desc",
        "pokemons": [{"pokemon": "pikachu", "hidden": False}],
        "descriptions": [{"version": "red"}],
    }
    model = PokemonAbility(payload)
    assert model.name == "static"
    assert model.pokemons[0].pokemon == "pikachu"
    assert model.descriptions[0].version == "red"


def test_pokemon_item_and_move_model() -> None:
    item = PokemonItem(
        {
            "name": "potion",
            "id": 1,
            "effects": "heal",
            "cost": 300,
            "attributes": ["usable-overworld"],
            "category": "medicine",
            "sprite": "https://example.com/sprite.png",
            "descriptions": [{"version": "red", "description": "heal hp"}],
        }
    )
    assert item.category == "medicine"

    move = PokemonMove(
        {
            "name": "thunderbolt",
            "id": 85,
            "effects": "damage",
            "generation": 1,
            "type": "electric",
            "category": "special",
            "contest": "cool",
            "pp": 15,
            "power": 90,
            "accuracy": 100,
            "pokemon": ["pikachu"],
            "descriptions": [{"version": "red", "description": "zap"}],
        }
    )
    assert move.power == 90


def test_pokedex_model() -> None:
    pokedex = PokeDex(
        {
            "name": "pikachu",
            "id": "25",
            "type": ["electric"],
            "species": ["mouse"],
            "abilities": ["static"],
            "height": "4",
            "base_experience": "112",
            "gender": ["male", "female"],
            "egg_groups": ["field"],
            "stats": {"hp": "35", "attack": "55", "defense": "40", "sp_atk": "50", "sp_def": "50", "speed": "90", "total": "320"},
            "family": {"evolutionStage": 2, "evolutionLine": ["pichu", "pikachu"]},
            "sprites": {"normal": "n", "animated": "a"},
            "description": "desc",
            "generation": "1",
        }
    )
    assert pokedex.name == "pikachu"
    assert pokedex.stats.total == "320"
    assert pokedex.family.evolution_stage == 2

