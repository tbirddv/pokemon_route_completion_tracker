from Data.constants import SupportedGames, Generation_1
import json
from pathlib import Path
from dataclasses import dataclass
from src.pokemon import Pokemon, Local_Gen1
from src.location import Location, Gen1Location

@dataclass
class GameSettings:
    game: SupportedGames

    @classmethod
    def from_dict(cls, data):
        game = SupportedGames(data['game'])
        return cls(game=game)
    
    def to_dict(self):
        return {
            'game': self.game.value
        }
@dataclass
class SaveData:
    pokemon: list[Pokemon]
    locations: list[Location]
    unavailable_pokemon: list[str]
    settings: GameSettings = None

    @classmethod
    def from_dict(cls, data):
        settings = GameSettings.from_dict(data['settings']) if 'settings' in data else None
        pokemon_data = data.get('pokemon', [])
        location_data = data.get('locations', [])
        unavailable_pokemon = data.get('unavailable_pokemon', [])

        if settings.game in Generation_1:
            pokemon_list = [Local_Gen1.from_dict(p) for p in pokemon_data]
            location_list = [Gen1Location.from_dict(l) for l in location_data]
        else:
            pokemon_list = [Pokemon.from_dict(p) for p in pokemon_data]
            location_list = [Location.from_dict(l) for l in location_data]

        return cls(
            settings=settings,
            pokemon=pokemon_list,
            locations=location_list,
            unavailable_pokemon=unavailable_pokemon
        )
    
    def to_dict(self):
        return {
            'settings': self.settings.to_dict() if self.settings else None,
            'pokemon': [p.to_dict() for p in self.pokemon],
            'locations': [l.to_dict() for l in self.locations],
            'unavailable_pokemon': self.unavailable_pokemon
        }


def get_game_enum(game_name):
    game_name = game_name.strip().upper()
    try:
        return SupportedGames[game_name]
    except KeyError:
        raise ValueError(f"Unsupported game name: {game_name}. Please see readme for currently supported games.")
    
def load_save_file(game_name):
    game = get_game_enum(game_name)
    save_file_path = Path.home() / f".pokemon_tracker/saves/{game.value}/save.json"
    if not save_file_path.exists():
        raise FileNotFoundError(f"No save file found for game: Pokemon {game.value}")
    with open(save_file_path, 'r', encoding='utf-8') as save_file:
        return SaveData.from_dict(json.load(save_file))
    
def save_game_data(game_name, save_data: SaveData):
    game = get_game_enum(game_name)
    save_file_path = Path.home() / f".pokemon_tracker/saves/{game.value}/save.json"
    if not save_file_path.parent.exists():
        raise FileNotFoundError(f"No save directory found for game: Pokemon {game.value}. Please create a new game first.")
    with open(save_file_path, 'w', encoding='utf-8') as save_file:
        json.dump(save_data.to_dict(), save_file, indent=4)
    print(f"Game data for Pokemon {game.value} updated successfully.")

    
