import argparse
import sys
import json
from pathlib import Path
from src.utils import get_game_enum, SaveData, save_game_data, load_save_file, change_tracked_game, load_app_config, update_app_config, AppConfig
from Data.constants import SupportedGames
from src.newgame import new_game, delete_game_save
from src.game_status_update import catch_pokemon, reset_pokemon_status, handle_evolution_tracking, handle_evolvable_reset, evolve_pokemon
from src.user_output import detailed_area_report, simple_area_report, basic_individual_pokemon_report, simple_completion_report, detailed_completion_report

def main():
    parser = argparse.ArgumentParser(
        description="Pokedex completion tracker",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    new_game_parser = subparsers.add_parser('new', help='Start tracking a new game')
    new_game_parser.add_argument('game_name', type=str, help='Name of the game to start tracking. Omit the word Pokemon (e.g., Red, Blue, Yellow)')
    new_game_parser.add_argument('-o', "--overwrite", action='store_true', help='Overwrite existing save file if it exists')
    new_game_parser.set_defaults(func=handle_new_game)

    delete_game_parser = subparsers.add_parser('delete', help='Delete an existing game save')
    delete_game_parser.add_argument('game_name', type=str, help='Name of the game to delete save for. Omit the word Pokemon (e.g., Red, Blue, Yellow)')
    delete_game_parser.set_defaults(func=handle_delete_game)

    change_config_parser = subparsers.add_parser('config', help='Make changes to the config, such as changing the tracked game')
    change_config_parser.add_argument('-l', '--list', action='store_true', help='List the current config settings')
    change_config_parser.add_argument('-g', '--game', action='store_true', help='Change the currently tracked game. Omit the word Pokemon (e.g., Red, Blue, Yellow)')
    change_config_parser.add_argument('-r', '--reset', action='store_true', help='Completely reset the config to default settings (no tracked game, companion tracker disabled, evolution tracking disabled) and delete all existing game saves')
    change_config_parser.add_argument('-c', '--companion_tracker', action='store_true', help='Toggle companion tracker setting in config to opposite of current setting')
    change_config_parser.add_argument('-e', '--evolution_track', action='store_true', help='Toggle evolution tracking setting in config to opposite of current setting. ')
    change_config_parser.add_argument('game_name', type=str, nargs='?', help='Name of the game to set as tracked. Omit the word Pokemon (e.g., Red, Blue, Yellow)')
    change_config_parser.set_defaults(func=handle_change_config)

    catch_parser = subparsers.add_parser('catch', help='Mark a Pokemon as caught')
    catch_parser.add_argument('pokemon_name', type=str, help='Name of the Pokemon to mark as caught')
    catch_parser.set_defaults(func=handle_catch_pokemon)

    evolve_parser = subparsers.add_parser('evolve', help='If called on a caught pokemon, mark its next evolution as caught. If called on an uncaught pokemon, mark it as caught.')
    evolve_parser.add_argument('pokemon_name', type=str, help='Name of the Pokemon to evolve (or evolved form to mark as caught)')
    evolve_parser.add_argument('--into', type=str, help='Specify the name of the evolution to mark as caught. Required if the specified Pokemon has multiple evolutions (e.g., Eevee). If not provided, the first evolution listed in the data file will be used.')
    evolve_parser.set_defaults(func=handle_evolve_pokemon)

    hatch_parser = subparsers.add_parser('hatch', help='Mark a Pokemon as caught via hatching (same as catch command, but for clarity)')
    hatch_parser.add_argument('pokemon_name', type=str, help='Name of the Pokemon to mark as caught via hatching')
    hatch_parser.set_defaults(func=handle_hatch_pokemon)

    reset_parser = subparsers.add_parser('reset', help='Reset a Pokemon\'s status to uncaught WARNING: This command also completely resets status for evolutions and devolutions of the specified Pokemon if evolution tracking is enabled in config')
    reset_parser.add_argument('pokemon_name', type=str, help='Name of the Pokemon to reset status for')
    reset_parser.set_defaults(func=handle_reset_pokemon)

    area_report_parser = subparsers.add_parser('area', help='Generate a report for a specific area')
    area_report_parser.add_argument('area_name', type=str, help='Name of the area to generate report for')
    report_complexity_group = area_report_parser.add_mutually_exclusive_group()
    report_complexity_group.add_argument('-S', '--simple', action='store_true', help='Generate a simple area report (caught and uncaught only)')
    area_report_parser.add_argument('-w', '--walking', action='store_true', help='Generate a detailed area report including walking encounters')
    area_report_parser.add_argument('-f', '--fishing', action='store_true', help='Generate a detailed area report including fishing encounters')
    area_report_parser.add_argument('-s', '--surfing', action='store_true', help='Generate a detailed area report including surfing encounters')
    area_report_parser.add_argument('-o', '--other', action='store_true', help='Generate a detailed area report including other encounter types')
    area_report_parser.add_argument('-C', '--companion-details', action='store_true', help='Include details for companion games in the report (if applicable)')
    area_report_parser.set_defaults(func=handle_area_report)

    pokemon_report_parser = subparsers.add_parser('pokemon-report', help='Generate a report for a specific Pokemon')
    pokemon_report_parser.add_argument('pokemon_name', type=str, help='Name of the Pokemon to generate report for')
    pokemon_report_parser.add_argument('-l', '--locations', action='store_true', help='Include location details in the report')
    pokemon_report_parser.set_defaults(func=handle_pokemon_report)

    completion_report_parser = subparsers.add_parser('completion', help='Generate a completion report for the tracked game')
    completion_report_parser.add_argument('-d', '--detailed', action='store_true', help='Generate a detailed completion report (caught, uncaught, and unavailable)')
    completion_report_parser.set_defaults(func=handle_completion_report)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)

def handle_new_game(args):
    new_game(args.game_name, overwrite=args.overwrite, cli_mode=True)

def handle_delete_game(args):
    delete_game_save(args.game_name)

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
    if args.simple:
        if not args.area_name:
            print("Please specify an area name for the report.")
            return
        simple_area_report(config.tracked_game.value, args.area_name, companion_mode=config.companion_tracker)
    else:
        if not args.area_name:
            print("Please specify an area name for the report.")
            return
        detailed_area_report(config.tracked_game.value, args.area_name, walking=args.walking, fishing=args.fishing, surfing=args.surfing, other=args.other, unavailable=config.companion_tracker, companion_details=args.companion_details)

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
    if args.detailed:
        detailed_completion_report(config.tracked_game.value, companion=config.companion_tracker)
    else:
        simple_completion_report(config.tracked_game.value)

if __name__ == "__main__":
    main()
