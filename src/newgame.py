import os
import csv
import json
from pathlib import Path
from src.pokemon import Local_Gen1
from src.location import Gen1Location
from Data.constants import SupportedGames, Generation_1

def get_game_enum(game_name):
    game_name = game_name.strip().upper()
    try:
        return SupportedGames[game_name]
    except KeyError:
        raise ValueError(f"Unsupported game name: {game_name}. Please see readme for currently supported games.")
    
def delete_game_save(game):
    if not isinstance(game, SupportedGames):
        game = get_game_enum(game)
    save_dir = Path.home() / f".pokemon_tracker/saves/{game.value}"
    if save_dir.exists() and save_dir.is_dir():
        for file in save_dir.glob('*'):
            file.unlink()
        save_dir.rmdir()
        print(f"Deleted save directory for {game.value}.")
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
        if not pokemon_path.exists() or not location_path.exists():
            raise FileNotFoundError("Required data files for Generation 1 not found.")
        print(f"Loading Generation 1 data from {pokemon_path} and {location_path}.")
        # Load Pokemon data
        pokemon_list = []
        location_list = []
        unavailable_pokemon = []
        with open(pokemon_path, mode='r', encoding='utf-8') as pokemon_file:
            pokemon_reader = csv.DictReader(pokemon_file)
            for row in pokemon_reader:
                pokemon = Local_Gen1(
                    name=row['Name'],
                    id=int(row['ID']),
                    red_routes=row['Red Routes'],
                    red_uniques=row['Red Uniques'],
                    blue_routes=row['Blue Routes'],
                    blue_uniques=row['Blue Uniques'],
                    yellow_routes=row['Yellow Routes'],
                    yellow_uniques=row['Yellow Uniques'],
                    devolutions=row['Devolutions'],
                    evolutions=row['Evolutions']
                )
                pokemon_list.append(pokemon)
        with open(location_path, mode='r', encoding='utf-8') as location_file:
            location_reader = csv.DictReader(location_file)
            for row in location_reader:
                if row['Area Name'].strip().lower() == 'unavailable':
                    raw_unavailable_str = row.get(f"{game.value} Walking", "")
                    unavailable = [p.strip() for p in raw_unavailable_str.split('/') if p.strip() and p.strip().lower() != 'none']
                    unavailable_pokemon.extend(unavailable)
                    continue
                location = Gen1Location(
                    name=row['Area Name'],
                    red_walking=row['Red Walking'],
                    red_surfing=row['Red Surfing'],
                    red_fishing=row['Red Fishing'],
                    red_other=row['Red Other'],
                    blue_walking=row['Blue Walking'],
                    blue_surfing=row['Blue Surfing'],
                    blue_fishing=row['Blue Fishing'],
                    blue_other=row['Blue Other'],
                    yellow_walking=row['Yellow Walking'],
                    yellow_surfing=row['Yellow Surfing'],
                    yellow_fishing=row['Yellow Fishing'],
                    yellow_other=row['Yellow Other']
                )
                location_list.append(location)
        # Save initial game state
        initial_save = {
            'game': game.value,
            'pokemon': [vars(p) for p in pokemon_list],
            'locations': [vars(l) for l in location_list],
            'unavailable_pokemon': unavailable_pokemon
        }
        with open(save_file_path, 'w', encoding='utf-8') as save_file:
            json.dump(initial_save, save_file, indent=4)
        print(f"New game save for Pokemon {game.value} created successfully.")

