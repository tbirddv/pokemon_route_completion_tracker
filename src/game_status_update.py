from src.utils import (get_game_enum, SaveData, save_game_data, load_save_file)
from Data.constants import SupportedGames, Generation_1
from src.pokemon import Pokemon, Local_Gen1
from src.location import Location, Gen1Location
            

def catch_pokemon(game_name, pokemon_name):
    game = get_game_enum(game_name)
    save_data = load_save_file(game.value)
    found = False
    for pokemon in save_data.pokemon:
        if pokemon.name.lower() == pokemon_name.lower():
            found = True
            if pokemon.status == "Caught":
                print(f"{pokemon.name} is already caught.")
                return
            pokemon.status = "Caught"
            print(f"Caught {pokemon.name}!")
            break
    if not found:
        print(f"Pokemon {pokemon_name} not found in the save data for {game.value}. Please ensure the correct game is loaded and that the Pokemon is found in that game.")
        return
    for location in save_data.locations:
        location.mark_pokemon_caught_in_area(pokemon.name)
    for unavailable in save_data.remaining_unavailable_pokemon:
        if unavailable.lower() == pokemon_name.lower():
            save_data.remaining_unavailable_pokemon.remove(unavailable)
            break

    save_game_data(game.value, save_data)

def reset_pokemon_status(game_name, pokemon_name):
    game = get_game_enum(game_name)
    save_data = load_save_file(game.value)
    found = False
    for pokemon in save_data.pokemon:
        if pokemon.name.lower() == pokemon_name.lower():
            pokemon.status = "Uncaught"
            print(f"Reset status of {pokemon.name} to Uncaught.")
            found = True
            break
    if not found:
        print(f"Pokemon {pokemon_name} not found in the save data for {game.value}. Please ensure the correct game is loaded and that the Pokemon is found in that game.")
        return
    for location in save_data.locations:
        location.reset_pokemon_status_in_area(pokemon.name)

    for unavailable in save_data.unavailable_pokemon:
        if unavailable.lower() == pokemon_name.lower():
            if unavailable not in save_data.remaining_unavailable_pokemon:
                save_data.remaining_unavailable_pokemon.append(unavailable)
            break

    save_game_data(game.value, save_data)
