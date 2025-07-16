from Data.constants import SupportedGames, Generation_1
import json
import sys
import shutil
from pathlib import Path
from dataclasses import dataclass
from src.pokemon import Pokemon, Local_Gen1
from src.location import Location, Gen1Location
from enum import Enum


class ObjectType(Enum):
    POKEMON = 'pokemon'
    LOCATION = 'location'


@dataclass
class GameSettings:
    game: SupportedGames
    surf: bool = False
    super_rod: bool = False
    good_rod: bool = False
    old_rod: bool = False

    @classmethod
    def from_dict(cls, data):
        game = SupportedGames(data['game'])
        surf = data.get('surf', False)
        super_rod = data.get('super_rod', False)
        good_rod = data.get('good_rod', False)
        old_rod = data.get('old_rod', False)
        return cls(game=game, surf=surf, super_rod=super_rod, good_rod=good_rod, old_rod=old_rod)
    
    def to_dict(self):
        return {
            'game': self.game.value,
            'surf': self.surf,
            'super_rod': self.super_rod,
            'good_rod': self.good_rod,
            'old_rod': self.old_rod
        }
    
@dataclass
class SaveData:
    pokemon: list[Pokemon]
    locations: list[Location]
    unavailable_pokemon: list[str]
    remaining_unavailable_pokemon: list[str] = None
    settings: GameSettings = None

    @classmethod
    def from_dict(cls, data):
        settings = GameSettings.from_dict(data['settings']) if 'settings' in data else None
        pokemon_data = data.get('pokemon', [])
        location_data = data.get('locations', [])
        unavailable_pokemon = data.get('unavailable_pokemon', [])
        remaining_unavailable_pokemon = data.get('remaining_unavailable_pokemon', [])

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
            unavailable_pokemon=unavailable_pokemon,
            remaining_unavailable_pokemon=remaining_unavailable_pokemon
        )
    
    def to_dict(self):
        return {
            'settings': self.settings.to_dict() if self.settings else None,
            'pokemon': [p.to_dict() for p in self.pokemon],
            'locations': [l.to_dict() for l in self.locations],
            'unavailable_pokemon': self.unavailable_pokemon,
            'remaining_unavailable_pokemon': self.remaining_unavailable_pokemon
        }

@dataclass
class AppConfig:
    tracked_game: SupportedGames = None
    companion_tracker: bool = False  # Whether to track companion games in area reports
    evolution_track: bool = False  # Whether to track evolutions in catch/reset operations

    @classmethod
    def from_dict(cls, data):
        tracked_game = SupportedGames(data['tracked_game']) if 'tracked_game' in data and data['tracked_game'] else None
        companion_tracker = data.get('companion_tracker', False)
        evolution_track = data.get('evolution_track', False)
        return cls(tracked_game=tracked_game, companion_tracker=companion_tracker, evolution_track=evolution_track)
    
    def to_dict(self):
        return {
            'tracked_game': self.tracked_game.value if self.tracked_game else None,
            'companion_tracker': self.companion_tracker,
            'evolution_track': self.evolution_track
        }

def get_game_enum(game_name):
    game_name = game_name.strip().upper()
    try:
        return SupportedGames[game_name]
    except KeyError:
        print(f"Unsupported game name: {game_name}. Please see readme for currently supported games.")
        sys.exit(1)

def get_backup_save_path(game_name:str) -> Path:
    game = get_game_enum(game_name)
    return Path.home() / f".pokemon_tracker/.backups/{game.value}/save_backup.json"
        

def load_save_file(game_name):
    game = get_game_enum(game_name)
    save_file_path = Path.home() / f".pokemon_tracker/saves/{game.value}/save.json"
    if not save_file_path.exists():
        print(f"No save file found for game: Pokemon {game.value}. Please create a new game first.")
        sys.exit(1)
    try:
        with open(save_file_path, 'r', encoding='utf-8') as save_file:
            return SaveData.from_dict(json.load(save_file))
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Error Loading save file for Pokemon {game.value}: {e}. Please ensure the save file is not corrupted.")
        if get_backup_save_path(game.value).exists():
            continue_prompt = input("A backup save file exists. Would you like to restore from the backup? (y/n): ").strip().lower()
            if continue_prompt != 'y':
                print("Aborting load operation. Please fix or delete the corrupted save file.")
                sys.exit(1)
            print("Restoring from backup save file...")
            try:
                shutil.copy2(get_backup_save_path(game.value), save_file_path)
                with open(save_file_path, 'r', encoding='utf-8') as save_file:
                    return SaveData.from_dict(json.load(save_file))
            except Exception as e:
                print(f"Failed to restore from backup: {e}. Please create a new game save.")
                sys.exit(1)
    
def save_game_data(game_name, save_data: SaveData):
    game = get_game_enum(game_name)
    save_file_path = Path.home() / f".pokemon_tracker/saves/{game.value}/save.json"
    backup_file_path = get_backup_save_path(game.value)
    if not save_file_path.parent.exists():
        print(f"No save directory found for game: Pokemon {game.value}. Please create a new game first.")
        sys.exit(1)
    if not backup_file_path.parent.exists():
        backup_file_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copy2(save_file_path, backup_file_path)
    except Exception as e:
        print(f"Warning: Could not create backup of save file. Error: {e}")
    try:
        with open(save_file_path, 'w', encoding='utf-8') as save_file:
            json.dump(save_data.to_dict(), save_file, indent=4)
    except OSError as e:
        print(f"Error saving game data for Pokemon {game.value}: {e}")
        sys.exit(1)

def load_app_config():
    config_path = Path.home() / ".pokemon_tracker/config.json"
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as config_file:
            json.dump({'tracked_game': None, 'companion_tracker': False, 'evolution_track': False}, config_file, indent=4)
        return AppConfig(tracked_game=None, companion_tracker=False, evolution_track=False)
    try:
        with open(config_path, 'r', encoding='utf-8') as config_file:
            return AppConfig.from_dict(json.load(config_file))
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Error loading config file: {e}. Resetting to default configuration.")
        with open(config_path, 'w', encoding='utf-8') as config_file:
            json.dump({'tracked_game': None, 'companion_tracker': False, 'evolution_track': False}, config_file, indent=4)
        return AppConfig(tracked_game=None, companion_tracker=False, evolution_track=False)
    except OSError as e:
        print(f"Error accessing config file: {e}. Please ensure the .pokemon_tracker directory is accessible.")
        sys.exit(1)
    
def update_app_config(config: AppConfig):
    config_path = Path.home() / ".pokemon_tracker/config.json"
    if not config_path.parent.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, 'w', encoding='utf-8') as config_file:
        json.dump(config.to_dict(), config_file, indent=4)

def change_tracked_game(game_name):
    game = get_game_enum(game_name) if game_name else None
    config = load_app_config()
    config.tracked_game = game
    update_app_config(config)
    if game:
        print(f"Now tracking Pokemon {game.value}.")
    else:
        print("No game is currently being tracked.")

def format_list_for_output(items, indent_level, max_width):
    if not items:
        return ""
    
    title_items = [item.title() for item in items]
    lines = []
    current_line = " " * indent_level
    for item in title_items:
        if len(current_line) + len(item) + 2 > max_width and len(current_line) > indent_level:
            lines.append(current_line.rstrip(", "))
            current_line = " " * indent_level + item
        else:
            if current_line == " " * indent_level:
                current_line += item
            else:
                item_with_comma = ", " + item
                current_line += item_with_comma
    lines.append(current_line.rstrip(", "))
    return "\n".join(lines)

def get_terminal_width(default=80):
    try:
        width = shutil.get_terminal_size().columns
        return width if width > 0 else default
    except Exception:
        return default

def get_object_from_save(save_data: SaveData, object_name: str, object_type: ObjectType):
    object_name = object_name.strip().lower()
    if object_type == ObjectType.POKEMON:
        for pokemon in save_data.pokemon:
            if pokemon.name == object_name:
                return pokemon
    elif object_type == ObjectType.LOCATION:
        for location in save_data.locations:
            if location.name.lower() == object_name:
                return location
    return None    
