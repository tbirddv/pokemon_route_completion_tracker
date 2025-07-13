from src.utils import (get_game_enum, SaveData, save_game_data, load_save_file)
from Data.constants import SupportedGames, Generation_1
from src.pokemon import Local_Gen1, Pokemon
from src.location import Gen1Location, Location

def area_report(game_name, area_name):
    game = get_game_enum(game_name)
    save_data = load_save_file(game.value)
    for location in save_data.locations:
        if location.name.lower() == area_name.lower():
            print(f"---Area Report for: {location.name} in Pokemon {game.value}---")
            print(f"Caught Pokemon: {', '.join(sorted(list(location.caught))) if location.caught else "None"}")
            uncaught_fields = location.uncaught_fields()
            print("Uncaught Pokemon in this game:")
            for game_in_generation in uncaught_fields.keys():
                if game_in_generation == game:
                    for encounter_type in uncaught_fields[game_in_generation].keys():
                        print(f"    {encounter_type}: ")
                        if isinstance(uncaught_fields[game_in_generation][encounter_type], dict):
                            for sublocation in uncaught_fields[game_in_generation][encounter_type].keys():
                                if sublocation.lower() != "main":
                                    print(f"      {sublocation}: ", end="")
                                else:
                                    print("      ", end="")
                                if isinstance(uncaught_fields[game_in_generation][encounter_type][sublocation], list):
                                    if not uncaught_fields[game_in_generation][encounter_type][sublocation]:
                                        print("None")
                                    else:
                                        print(", ".join(uncaught_fields[game_in_generation][encounter_type][sublocation]))
                                if isinstance(uncaught_fields[game_in_generation][encounter_type][sublocation], dict):
                                    for subtype in uncaught_fields[game_in_generation][encounter_type][sublocation].keys():
                                        if not uncaught_fields[game_in_generation][encounter_type][sublocation][subtype]:
                                            print(f"    {subtype}: None")
                                        else:
                                            print(f"    {subtype}: ", end="")
                                            print(", ".join(uncaught_fields[game_in_generation][encounter_type][sublocation][subtype]))
                    break
            print("Pokemon unavailable in this game found in this area of companion games:")
            for game_in_generation in uncaught_fields.keys():
                if game_in_generation != game:
                    print(f"{game_in_generation.value}:")
                    companion_game_pokemon = set()
                    for pokemon in save_data.unavailable_pokemon:
                        if pokemon in location.caught:
                            continue
                        for encounter_type in uncaught_fields[game_in_generation].keys():
                            if isinstance(uncaught_fields[game_in_generation][encounter_type], dict):
                                for sublocation in uncaught_fields[game_in_generation][encounter_type].keys():
                                    if isinstance(uncaught_fields[game_in_generation][encounter_type][sublocation], list):
                                        if pokemon in uncaught_fields[game_in_generation][encounter_type][sublocation]:
                                            companion_game_pokemon.add(pokemon)
                                    if isinstance(uncaught_fields[game_in_generation][encounter_type][sublocation], dict):
                                        for subtype in uncaught_fields[game_in_generation][encounter_type][sublocation].keys():
                                            if pokemon in uncaught_fields[game_in_generation][encounter_type][sublocation][subtype]:
                                                companion_game_pokemon.add(pokemon)
                            if isinstance(uncaught_fields[game_in_generation][encounter_type], list):
                                if pokemon in uncaught_fields[game_in_generation][encounter_type]:
                                    companion_game_pokemon.add(pokemon)
                    if companion_game_pokemon:
                        print(f"    {', '.join(sorted(list(companion_game_pokemon)))}")
                    else:
                        print("    None")
            return
    print(f"Area {area_name} not found in save data for game {game.value}.")
