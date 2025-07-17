from src.utils import get_game_enum, SaveData, save_game_data, load_save_file, get_object_from_save, ObjectType
from Data.constants import SupportedGames, Generation_1, complex_evolutions
from src.pokemon import Pokemon, Local_Gen1
from src.location import Location, Gen1Location, ModificationType
            

def handle_evolution_tracking(game: SupportedGames, save_data: SaveData, found_pokemon: Pokemon):
    for evolution_name in getattr(found_pokemon, 'evolutions', []):
            evolution_pokemon = get_object_from_save(save_data, evolution_name, ObjectType.POKEMON)
            if evolution_pokemon and evolution_pokemon.status != "Caught":
                evolution_pokemon.status = "Evolvable"
                for location in save_data.locations:
                    location.update_pokemon_status_in_area(evolution_pokemon.name, modification_type=ModificationType.EVOLVABLE)
                if evolution_pokemon.name in save_data.remaining_unavailable_pokemon:
                    save_data.remaining_unavailable_pokemon.remove(evolution_pokemon.name)
            if game not in Generation_1:
                for devolution_name in getattr(found_pokemon, 'devolutions', []):
                    devolution_pokemon = get_object_from_save(save_data, devolution_name, ObjectType.POKEMON)
                    if devolution_pokemon and devolution_pokemon.status not in ["Caught", "Evolvable"]:
                        devolution_pokemon.status = "Devolvable"
                        for location in save_data.locations:
                            location.update_pokemon_status_in_area(devolution_pokemon.name, modification_type=ModificationType.DEVOLVABLE)
                        if devolution_pokemon.name in save_data.remaining_unavailable_pokemon:
                            save_data.remaining_unavailable_pokemon.remove(devolution_pokemon.name)

def handle_evolvable_reset(game: SupportedGames, save_data: SaveData, found_pokemon: Pokemon, config_mode=False):
    for evolution_name in getattr(found_pokemon, 'evolutions', []):
            evolution_pokemon = get_object_from_save(save_data, evolution_name, ObjectType.POKEMON)
            if evolution_pokemon and evolution_pokemon.status != "Uncaught":
                if not config_mode:
                    print(f"Also resetting evolution {evolution_pokemon.name.title()} to Uncaught.")
                evolution_pokemon.status = "Uncaught"
                for location in save_data.locations:
                    location.reset_pokemon_status_in_area(evolution_pokemon.name)
                if evolution_pokemon.name in save_data.unavailable_pokemon and evolution_pokemon.name not in save_data.remaining_unavailable_pokemon:
                    save_data.remaining_unavailable_pokemon.append(evolution_pokemon.name)
    if game not in Generation_1:
        for devolution_name in getattr(found_pokemon, 'devolutions', []):
            devolution_pokemon = get_object_from_save(save_data, devolution_name, ObjectType.POKEMON)
            if devolution_pokemon and devolution_pokemon.status != "Uncaught":
                if not config_mode:
                    print(f"Also resetting devolution {devolution_pokemon.name.title()} to Uncaught.")
                devolution_pokemon.status = "Uncaught"
                for location in save_data.locations:
                    location.reset_pokemon_status_in_area(devolution_pokemon.name)
                if devolution_pokemon.name in save_data.unavailable_pokemon and devolution_pokemon.name not in save_data.remaining_unavailable_pokemon:
                    save_data.remaining_unavailable_pokemon.append(devolution_pokemon.name)

def catch_pokemon(game_name, pokemon_name, evolution_track=False, breed_baby=False):
    game = get_game_enum(game_name)
    save_data = load_save_file(game.value)
    pokemon_name = pokemon_name.strip().lower()
    found_pokemon = get_object_from_save(save_data, pokemon_name, ObjectType.POKEMON)
    if not found_pokemon:
        print(f"Pokemon {pokemon_name} not found in the save data for {game.value}. Please ensure the correct game is loaded and that the Pokemon is found in that game.")
        return
    if found_pokemon.status == "Caught":
        print(f"Pokemon {found_pokemon.name} is already marked as caught in {game.value}. No changes made.")
        return
    found_pokemon.status = "Caught"
    
    if not breed_baby:
        print(f"{pokemon_name.title()} caught!")
    else:
        print(f"You hatched a {pokemon_name.title()} from an egg!")
    
    for location in save_data.locations:
        location.update_pokemon_status_in_area(found_pokemon.name)
    
    if found_pokemon.name in save_data.remaining_unavailable_pokemon:
        save_data.remaining_unavailable_pokemon.remove(found_pokemon.name)
    
    if evolution_track:
        handle_evolution_tracking(game, save_data, found_pokemon)

    save_game_data(game.value, save_data)

def evolve_pokemon(game_name, pokemon_name, evolved_pokemon_name=None):
    """
    Evolves a Pokemon by marking it as caught and updating its status and locations accordingly.
    This is only intended to be called either on a pokemon to be evolved or on a pokemon that has just been evolved.
    As such the entire evolution chain should already have the appropriate statuses except the evolving form. So rechecking status of pokemon in evolutions/devolutions fields should not be necessary.
    Arguments:
        game_name: Name of the game the pokemon is in (e.g., "Red", "Blue", "Yellow")
        pokemon_name: Name of the pokemon to evolve (e.g., "Pikachu", "Charmander")
        evolved_pokemon_name: Optional name of the pokemon to evolve into (e.g., "Raichu", "Charmeleon"). If not provided, will use the first evolution in the evolutions list unless pokemon has complex evolutions.
            If the pokemon has complex evolutions (e.g., Eevee), this parameter must be provided to specify which evolution to evolve into.
    Returns:
        None
    """
    game = get_game_enum(game_name)
    save_data = load_save_file(game.value)
    pokemon_name = pokemon_name.strip().lower()
    if evolved_pokemon_name:
        evolved_pokemon_name = evolved_pokemon_name.strip().lower()
    found_pokemon = get_object_from_save(save_data, pokemon_name, ObjectType.POKEMON)
    
    if not found_pokemon:
        print(f"Pokemon {pokemon_name} not found in the save data for {game.value}. Please ensure the correct game is loaded and that the Pokemon is found in that game.")
        return
    
    if found_pokemon.status == "Evolvable":
        found_pokemon.status = "Caught"
        print(f"{found_pokemon.name.title()} evolved from {found_pokemon.devolutions[-1].title()}")
        for location in save_data.locations:
            location.update_pokemon_status_in_area(found_pokemon.name, modification_type=ModificationType.EVOLVE)
    
    elif found_pokemon.status == "Uncaught":
        if found_pokemon.devolutions:
            next_devolution = get_object_from_save(save_data, found_pokemon.devolutions[-1], ObjectType.POKEMON)
            if next_devolution.status == "Caught":
                found_pokemon.status = "Caught"
                print(f"{found_pokemon.name.title()} evolved from {next_devolution.name.title()}")
                for location in save_data.locations:
                    location.update_pokemon_status_in_area(found_pokemon.name, modification_type=ModificationType.EVOLVE)
            else:
                print(f"Cannot evolve {found_pokemon.name.title()} because its pre-evolution {next_devolution.name.title()} is not marked as caught.")
                print(f"No changes made. Please catch or evolve {next_devolution.name.title()} first.")
                return
        else:
            print(f"Nothing evolves into {found_pokemon.name.title()} and it is marked as Uncaught.")
            if found_pokemon.evolutions:
                print(f"If you want to evolve {found_pokemon.name.title()} into {found_pokemon.evolutions[0].title()}, please mark it as Caught first.")
            print(f"No changes made.")
            return
    
    elif found_pokemon.status == "Caught":
        if found_pokemon.evolutions:
            if not evolved_pokemon_name:
                if game in Generation_1 and found_pokemon.name in complex_evolutions['gen_1']:
                    print(f"Pokemon {found_pokemon.name.title()} has multiple possible evolutions. Please specify which evolution to evolve into using the --into argument")
                    print(f"Possible evolutions are: {', '.join([evo.title() for evo in found_pokemon.evolutions])}. No changes made.")
                    return
                evolved_pokemon_name = found_pokemon.evolutions[0]
            
            if evolved_pokemon_name not in found_pokemon.evolutions:
                print(f"Pokemon {found_pokemon.name.title()} cannot evolve into {evolved_pokemon_name.title()}. Possible evolutions are: {', '.join([evo.title() for evo in found_pokemon.evolutions])}. No changes made.")
                return
            
            evolved_pokemon = get_object_from_save(save_data, evolved_pokemon_name, ObjectType.POKEMON)
            
            if not evolved_pokemon:
                print(f"Evolved form {evolved_pokemon_name.title()} not found in the save data for {game.value}. Save data may be corrupted or incomplete.")
                return
            
            if evolved_pokemon.status == "Caught":
                print(f"Evolved form of {found_pokemon.name.title()} is already marked as caught.")
                print(f"No changes made.")
                return
            
            if evolved_pokemon.status != "Caught":
                evolved_pokemon.status = "Caught"
                print(f"{found_pokemon.name.title()} evolved into {evolved_pokemon.name.title()}")
                for location in save_data.locations:
                    location.update_pokemon_status_in_area(evolved_pokemon.name, modification_type=ModificationType.EVOLVE)
            
    
    else:
        print(f"No pokemon in the evolution chain of {found_pokemon.name.title()} is marked as Caught.")
        print(f"No changes made. Please ensure that a pokemon in this evolution chain is marked as Caught before using this command.")
    
    save_game_data(game.value, save_data)

def reset_pokemon_status(game_name, pokemon_name, evolution_track=False):
    """
    Resets a Pokemon's status to "Uncaught" and updates its status in all locations accordingly.
    If evolution_track is True, it will also reset the status of all evolutions and devolutions of the specified Pokemon to "Uncaught".
    Arguments:
        game_name: Name of the game the pokemon is in (e.g., "Red", "Blue", "Yellow")
        pokemon_name: Name of the pokemon to reset (e.g., "Pikachu", "Charmander")
        evolution_track: Boolean indicating whether to also reset the status of evolutions and devolutions of the specified Pokemon.
    Returns:
        None
    """
    pokemon_name = pokemon_name.strip().lower()
    game = get_game_enum(game_name)
    save_data = load_save_file(game.value)
    found_pokemon = get_object_from_save(save_data, pokemon_name, ObjectType.POKEMON)
    
    if not found_pokemon:
        print(f"Pokemon {pokemon_name} not found in the save data for {game.value}. Please ensure the correct game is loaded and that the Pokemon is found in that game.")
        return
    found_pokemon.status = "Uncaught"
    print(f"Reset status of {found_pokemon.name.title()} to Uncaught.")
    for location in save_data.locations:
        location.reset_pokemon_status_in_area(found_pokemon.name)

    if found_pokemon.name in save_data.unavailable_pokemon and found_pokemon.name not in save_data.remaining_unavailable_pokemon:
        save_data.remaining_unavailable_pokemon.append(found_pokemon.name)

    if evolution_track:
        handle_evolvable_reset(game, save_data, found_pokemon)

    save_game_data(game.value, save_data)
