import argparse
import sys
from src.utils import get_game_enum, SaveData, save_game_data, load_save_file, change_tracked_game, load_app_config, update_app_config, AppConfig
from Data.constants import SupportedGames
from src.newgame import new_game, delete_game_save
from src.game_status_update import catch_pokemon, reset_pokemon_status
from src.user_output import detailed_area_report, simple_area_report, basic_individual_pokemon_report

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
    change_config_parser.add_argument('-r', '--reset', action='store_true', help='Reset the config to default settings (no tracked game)')
    change_config_parser.add_argument('-c', '--companion_tracker', action='store_true', help='Toggle companion tracker setting in config to opposite of current setting')
    change_config_parser.add_argument('game_name', type=str, nargs='?', help='Name of the game to set as tracked. Omit the word Pokemon (e.g., Red, Blue, Yellow)')
    change_config_parser.set_defaults(func=handle_change_config)

    catch_parser = subparsers.add_parser('catch', help='Mark a Pokemon as caught')
    catch_parser.add_argument('pokemon_name', type=str, help='Name of the Pokemon to mark as caught')
    catch_parser.set_defaults(func=handle_catch_pokemon)

    reset_parser = subparsers.add_parser('reset', help='Reset a Pokemon\'s status to uncaught')
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
    if args.reset:
        update_app_config(AppConfig(tracked_game=None, companion_tracker=False))
        print("Config reset to default settings (no tracked game, companion tracker disabled).")
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
    catch_pokemon(config.tracked_game.value, args.pokemon_name)

def handle_reset_pokemon(args):
    config = load_app_config()
    if config.tracked_game is None:
        print("No game currently being tracked. Please set a game using the 'change' command.")
        return
    reset_pokemon_status(config.tracked_game.value, args.pokemon_name)

def handle_area_report(args):
    config = load_app_config()
    if config.tracked_game is None:
        print("No game currently being tracked. Please set a game using the 'change' command.")
        return
    if args.simple:
        if not args.area_name:
            print("Please specify an area name for the report.")
            return
        simple_area_report(config.tracked_game.value, args.area_name)
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

if __name__ == "__main__":
    main()
