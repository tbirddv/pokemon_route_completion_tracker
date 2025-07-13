import argparse
import sys
from src.utils import get_game_enum, SaveData, save_game_data, load_save_file, change_tracked_game, load_app_config
from Data.constants import SupportedGames
from src.newgame import new_game, delete_game_save
from src.game_status_update import catch_pokemon, reset_pokemon_status
from src.user_output import area_report

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

    change_game_parser = subparsers.add_parser('change', help='Change the current game being tracked')
    change_game_parser.add_argument('game_name', type=str, help='Name of the game to switch to. Omit the word Pokemon (e.g., Red, Blue, Yellow)')
    change_game_parser.set_defaults(func=handle_change_game)
    
    catch_parser = subparsers.add_parser('catch', help='Mark a Pokemon as caught')
    catch_parser.add_argument('pokemon_name', type=str, help='Name of the Pokemon to mark as caught')
    catch_parser.set_defaults(func=handle_catch_pokemon)

    reset_parser = subparsers.add_parser('reset', help='Reset a Pokemon\'s status to uncaught')
    reset_parser.add_argument('pokemon_name', type=str, help='Name of the Pokemon to reset status for')
    reset_parser.set_defaults(func=handle_reset_pokemon)

    area_report_parser = subparsers.add_parser('area', help='Generate a report for a specific area')
    area_report_parser.add_argument('area_name', type=str, help='Name of the area to generate report for')
    area_report_parser.set_defaults(func=handle_area_report)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)

def handle_new_game(args):
    new_game(args.game_name, overwrite=args.overwrite, cli_mode=True)

def handle_delete_game(args):
    delete_game_save(args.game_name)

def handle_change_game(args):
    change_tracked_game(args.game_name)

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
    area_report(config.tracked_game.value, args.area_name)

if __name__ == "__main__":
    main()
