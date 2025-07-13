from Data.constants import SupportedGames, Generation_1
import json
import sys
import shutil
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

@dataclass
class AppConfig:
    tracked_game: SupportedGames = None

    @classmethod
    def from_dict(cls, data):
        tracked_game = SupportedGames(data['tracked_game']) if 'tracked_game' in data and data['tracked_game'] else None
        return cls(tracked_game=tracked_game)
    
    def to_dict(self):
        return {
            'tracked_game': self.tracked_game.value if self.tracked_game else None
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
            json.dump({'tracked_game': None}, config_file, indent=4)
        return AppConfig(tracked_game=None)
    try:
        with open(config_path, 'r', encoding='utf-8') as config_file:
            return AppConfig.from_dict(json.load(config_file))
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Error loading config file: {e}. Resetting to default configuration.")
        with open(config_path, 'w', encoding='utf-8') as config_file:
            json.dump({'tracked_game': None}, config_file, indent=4)
        return AppConfig(tracked_game=None)
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

    
