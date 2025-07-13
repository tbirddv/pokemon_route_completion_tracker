import csv
import json
import sys
from pathlib import Path
from src.pokemon import Local_Gen1, Pokemon
from src.location import Gen1Location, Location
from src.utils import get_game_enum, change_tracked_game, load_app_config
from Data.constants import SupportedGames, Generation_1


    
def delete_game_save(game):
    if not isinstance(game, SupportedGames):
        game = get_game_enum(game)
    save_dir = Path.home() / f".pokemon_tracker/saves/{game.value}"
    if save_dir.exists() and save_dir.is_dir():
        for file in save_dir.glob('*'):
            file.unlink()
        save_dir.rmdir()
        print(f"Deleted save directory for {game.value}.")
        config = load_app_config()
        if config.tracked_game == game:
            change_tracked_game(None)
    else:
        print(f"No save directory found for {game.value} to delete.")

def new_game(game_name, overwrite=False, cli_mode=False):
    game = get_game_enum(game_name)
    save_dir = Path.home() / f".pokemon_tracker/saves/{game.value}"
    print(f"Creating new game save for Pokemon {game.value}")
    try:
        save_dir.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        if overwrite:
            print(f"Overwriting existing save for {game.value}.")
            delete_game_save(game)
            save_dir.mkdir(parents=True, exist_ok=True)
        else:   
            if not cli_mode:
                overwrite_prompt = input(f"A save for Pokemon {game.value} already exists. Overwrite? (y/n): ").strip().lower()
                if overwrite_prompt != 'y':
                    print("Game save already exists. Aborting new game creation.")
                    return None
                if overwrite_prompt == 'y':
                    delete_game_save(game)
                    save_dir.mkdir(parents=True, exist_ok=True)
            else:
                print(f"Game save for Pokemon {game.value} already exists. Please use -h or --help for CLI options.")
                return None
    # Initialize save file
    save_file_path = save_dir / 'save.json'
    if game in Generation_1:
        pokemon_path = Path.cwd() / 'Data/Pokemon/local_gen_1.csv'
        location_path = Path.cwd() / 'Data/Locations/kanto_gen_1.csv'
        if not pokemon_path.exists():
            print(f"Error: Pokemon data file for Generation 1 not found at {pokemon_path}. Cannot create new game save.")
            sys.exit(1)
        if not location_path.exists():
            print(f"Error: Location data file for Generation 1 not found at {location_path}. Cannot create new game save.")
            sys.exit(1)
        print(f"Loading Generation 1 data from {pokemon_path} and {location_path}.")
        # Load Pokemon data
        pokemon_list = []
        location_list = []
        unavailable_pokemon = []
        with open(pokemon_path, mode='r', encoding='utf-8-sig') as pokemon_file:
            pokemon_reader = csv.DictReader(pokemon_file)
            for row in pokemon_reader:
                pokemon = Local_Gen1.from_csv(row)
                pokemon_list.append(pokemon)
        with open(location_path, mode='r', encoding='utf-8-sig') as location_file:
            location_reader = csv.DictReader(location_file)
            for row in location_reader:
                if row['Area Name'].strip().lower() == 'unavailable':
                    raw_unavailable_str = row.get(f"{game.value} Walking", "")
                    unavailable = [p.strip().lower() for p in raw_unavailable_str.split('/') if p.strip() and p.strip().lower() != 'none']
                    unavailable_pokemon.extend(unavailable)
                    continue
                location = Gen1Location.from_csv(row)
                location_list.append(location)
        # Save initial game state
        initial_save = {
            'settings': {
                'game': game.value
            },
            'pokemon': [p.to_dict() for p in pokemon_list],
            'locations': [l.to_dict() for l in location_list],
            'unavailable_pokemon': unavailable_pokemon,
            'remaining_unavailable_pokemon': unavailable_pokemon.copy()
        }
        with open(save_file_path, 'w', encoding='utf-8') as save_file:
            json.dump(initial_save, save_file, indent=4)
        print(f"New game save for Pokemon {game.value} created successfully.")
    change_tracked_game(game.value)

