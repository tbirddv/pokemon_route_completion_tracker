import json
import random
from pathlib import Path
from src.utils import get_game_enum, SaveData, save_game_data, load_save_file, change_tracked_game, load_app_config, update_app_config, AppConfig
from Data.constants import SupportedGames
from src.newgame import new_game, delete_game_save
from src.game_status_update import catch_pokemon, reset_pokemon_status, handle_evolution_tracking, handle_evolvable_reset, evolve_pokemon
from src.user_output import (
    detailed_area_report, simple_area_report,
    basic_individual_pokemon_report, show_remaining_exclusives,
    simple_completion_report, detailed_completion_report,
    build_completion_report_by_area, items_needed_for_area_report   
)

def handle_new_game(args):
    new_game(args.game_name, overwrite=args.overwrite, cli_mode=True)

def handle_delete_game(args):
    if args.game_name:
        delete_game_save(args.game_name)
    else:
        config = load_app_config()
        if config.tracked_game is None:
            print("No game currently being tracked. Please specify a game name to delete.")
            return
        delete_game_save(config.tracked_game)
        print(f"Deleted save for currently tracked game: Pokemon {config.tracked_game.value}.")
        config.tracked_game = None
        update_app_config(config)

def handle_change_config(args):
    if args.companion_tracker:
        config = load_app_config()
        if not config.companion_tracker:
            config.companion_tracker = True
            print("Companion tracker setting enabled in config.")
        else:
            config.companion_tracker = False
            print("Companion tracker setting disabled in config.")
        update_app_config(config)
        return
    if args.evolution_track:
        config = load_app_config()
        saves_dir = Path.home() / ".pokemon_tracker/saves"
        if not config.evolution_track:
            config.evolution_track = True
            if saves_dir.exists() and saves_dir.is_dir():
                for game_dir in saves_dir.iterdir():
                    if game_dir.is_dir():
                        save_file = game_dir / 'save.json'
                        if save_file.exists():
                            with open(save_file, 'r', encoding='utf-8') as f:
                                save_data = SaveData.from_dict(json.load(f))
                                # Process save_data for evolution tracking
                                for pokemon in save_data.pokemon:
                                    if pokemon.status == "Caught":
                                        handle_evolution_tracking(get_game_enum(game_dir.name), save_data, pokemon)
                            with open(save_file, 'w', encoding='utf-8') as f:
                                json.dump(save_data.to_dict(), f, indent=4)
            print("Evolution tracking setting enabled in config.")
        else:
            config.evolution_track = False
            if saves_dir.exists() and saves_dir.is_dir():
                for game_dir in saves_dir.iterdir():
                    if game_dir.is_dir():
                        save_file = game_dir / 'save.json'
                        if save_file.exists():
                            with open(save_file, 'r', encoding='utf-8') as f:
                                save_data = SaveData.from_dict(json.load(f))
                                # Process save_data to reset evolvable Pokemon
                                for pokemon in save_data.pokemon:
                                    if pokemon.status == "Caught":
                                        handle_evolvable_reset(get_game_enum(game_dir.name), save_data, pokemon, config_mode=True)
                            with open(save_file, 'w', encoding='utf-8') as f:
                                json.dump(save_data.to_dict(), f, indent=4)
            print("Evolution tracking setting disabled in config.")
        update_app_config(config)
        return
    if args.reset:
        update_app_config(AppConfig(tracked_game=None, companion_tracker=False, evolution_track=False))
        saves_dir = Path.home() / ".pokemon_tracker/saves"
        if saves_dir.exists() and saves_dir.is_dir():
            for game_dir in saves_dir.iterdir():
                if game_dir.is_dir():
                    save_file = game_dir / 'save.json'
                    if save_file.exists():
                        save_file.unlink()
                    game_dir.rmdir()
            saves_dir.rmdir()
            print("All existing game saves deleted.")
        print("Config reset to default settings (no tracked game, companion tracker disabled, evolution tracking disabled).")
        return
    if args.list:
        config = load_app_config()
        print(config.to_dict())
        return
    if args.game:
        if not args.game_name:
            print("Please provide a game name when using the -g/--game option.")
            return
        else:
            change_tracked_game(args.game_name)
            return

def handle_item_change(args):
    config = load_app_config()
    if config.tracked_game is None:
        print("No game currently being tracked. Please set a game using the 'change' command.")
        return
    save_data = load_save_file(config.tracked_game.value)
    settings_changed = False
    if args.surf:
        save_data.settings.surf = not save_data.settings.surf
        print(f"Surf status for Pokemon {config.tracked_game.value} set to {save_data.settings.surf}.")
        settings_changed = True
    if args.super_rod:
        save_data.settings.super_rod = not save_data.settings.super_rod
        print(f"Super Rod status for Pokemon {config.tracked_game.value} set to {save_data.settings.super_rod}.")
        settings_changed = True
    if args.good_rod:
        save_data.settings.good_rod = not save_data.settings.good_rod
        print(f"Good Rod status for Pokemon {config.tracked_game.value} set to {save_data.settings.good_rod}.")
        settings_changed = True
    if args.old_rod:
        save_data.settings.old_rod = not save_data.settings.old_rod
        print(f"Old Rod status for Pokemon {config.tracked_game.value} set to {save_data.settings.old_rod}.")
        settings_changed = True
    if settings_changed:
        save_game_data(config.tracked_game.value, save_data)
    else:
        print("No item settings were changed. Please specify at least one item option to toggle.")

def handle_catch_pokemon(args):
    config = load_app_config()
    if config.tracked_game is None:
        print("No game currently being tracked. Please set a game using the 'change' command.")
        return
    catch_pokemon(config.tracked_game.value, args.pokemon_name, evolution_track=config.evolution_track)

def handle_evolve_pokemon(args):
    config = load_app_config()
    if config.tracked_game is None:
        print("No game currently being tracked. Please set a game using the 'change' command.")
        return
    evolve_pokemon(config.tracked_game.value, args.pokemon_name, evolved_pokemon_name=args.into)

def handle_hatch_pokemon(args):
    config = load_app_config()
    if config.tracked_game is None:
        print("No game currently being tracked. Please set a game using the 'change' command.")
        return
    catch_pokemon(config.tracked_game.value, args.pokemon_name, evolution_track=False, breed_baby=True)

def handle_reset_pokemon(args):
    config = load_app_config()
    if config.tracked_game is None:
        print("No game currently being tracked. Please set a game using the 'change' command.")
        return
    reset_pokemon_status(config.tracked_game.value, args.pokemon_name, evolution_track=config.evolution_track)

def handle_area_report(args):
    config = load_app_config()
    if config.tracked_game is None:
        print("No game currently being tracked. Please set a game using the 'change' command.")
        return
    if args.area_name.lower() == "random" or args.area_name.lower() == "-r":
        save_data = load_save_file(config.tracked_game.value)
        if not save_data.locations:
            print(f"No locations found for Pokemon {config.tracked_game.value}. Cannot select a random area.")
            return
        args.area_name = random.choice([loc.name for loc in save_data.locations if loc.encounter_data[config.tracked_game.value]['uncaught']['All']])
        print(f"Randomly selected area: {args.area_name}")
    if args.simple:
        simple_area_report(config.tracked_game.value, args.area_name, companion_mode=config.companion_tracker)
    elif args.items_needed:
        items_needed_for_area_report(config.tracked_game.value, args.area_name)
    else:
        if not (args.walking or args.fishing or args.surfing or args.other or args.all):
            save_data=load_save_file(config.tracked_game.value)
            kwargs = {"walking": True, "surfing": save_data.settings.surf, "super_rod": save_data.settings.super_rod, "good_rod": save_data.settings.good_rod, "old_rod": save_data.settings.old_rod, "other": True, "companion_tracking": config.companion_tracker, "companion_details": args.companion_details}
        elif args.all:
            kwargs = {"walking": True, "surfing": True, "super_rod": True, "good_rod": True, "old_rod": True, "other": True, "companion_tracking": config.companion_tracker, "companion_details": args.companion_details}
        else:
            kwargs = {"walking": args.walking, "surfing": args.surfing, "super_rod": args.fishing, "good_rod": args.fishing, "old_rod": args.fishing, "other": args.other, "companion_tracking": config.companion_tracker, "companion_details": args.companion_details}
        detailed_area_report(config.tracked_game.value, args.area_name, **kwargs)

def handle_pokemon_report(args):
    config = load_app_config()
    if config.tracked_game is None:
        print("No game currently being tracked. Please set a game using the 'change' command.")
        return
    if not args.pokemon_name:
        print("Please specify a Pokemon name for the report.")
        return
    basic_individual_pokemon_report(config.tracked_game.value, args.pokemon_name, location=args.locations, companions=config.companion_tracker)

def handle_completion_report(args):
    config = load_app_config()
    if config.tracked_game is None:
        print("No game currently being tracked. Please set a game using the 'change' command.")
        return
    if args.areas:
        if args.detailed:
            build_completion_report_by_area(config.tracked_game.value, detailed=True)
        else:
            build_completion_report_by_area(config.tracked_game.value, detailed=False)
        return
    if args.detailed:
        detailed_completion_report(config.tracked_game.value, companion=config.companion_tracker)
    else:
        simple_completion_report(config.tracked_game.value)

def handle_exclusives(args):
    config = load_app_config()
    if config.tracked_game is None:
        print("No game currently being tracked. Please set a game using the 'change' command.")
        return
    show_remaining_exclusives(config.tracked_game.value)