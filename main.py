#!/usr/bin/env python3
import argparse
import sys
from src.parser_handlers import (
    handle_new_game, handle_delete_game, handle_change_config, handle_item_change,
    handle_catch_pokemon, handle_evolve_pokemon, handle_hatch_pokemon, handle_reset_pokemon,
    handle_area_report, handle_pokemon_report, handle_completion_report, handle_exclusives
)

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

    change_item_parser = subparsers.add_parser('item', help='Change item settings for the current game (e.g., surf, fishing rods).')
    change_item_parser.add_argument('-s', '--surf', action='store_true', help='Toggle surf status for the current game (if applicable)')
    change_item_parser.add_argument('-SR', '--super-rod', action='store_true', help='Toggle super rod status for the current game (if applicable)')
    change_item_parser.add_argument('-GR', '--good-rod', action='store_true', help='Toggle good rod status for the current game (if applicable)')
    change_item_parser.add_argument('-OR', '--old-rod', action='store_true', help='Toggle old rod status for the current game (if applicable)')
    change_item_parser.set_defaults(func=handle_item_change)

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

    reset_parser = subparsers.add_parser('reset-pokemon', help='Reset a Pokemon\'s status to uncaught WARNING: This command also completely resets status for evolutions and devolutions of the specified Pokemon if evolution tracking is enabled in config')
    reset_parser.add_argument('pokemon_name', type=str, help='Name of the Pokemon to reset status for')
    reset_parser.set_defaults(func=handle_reset_pokemon)

    area_report_parser = subparsers.add_parser('area', help='Generate a report for a specific area')
    area_report_parser.add_argument('area_name', type=str, help='Name of the area to generate report for')
    report_complexity_group = area_report_parser.add_mutually_exclusive_group()
    report_complexity_group.add_argument('-S', '--simple', action='store_true', help='Generate a simple area report (caught and uncaught only)')
    item_needed_group = area_report_parser.add_mutually_exclusive_group()
    item_needed_group.add_argument('-i', '--items-needed', action='store_true', help='Generates a report of items needed to complete the area. Split into had and needed based on game save data')
    area_report_parser.add_argument('-w', '--walking', action='store_true', help='Generate a detailed area report including walking encounters')
    area_report_parser.add_argument('-f', '--fishing', action='store_true', help='Generate a detailed area report including fishing encounters')
    area_report_parser.add_argument('-s', '--surfing', action='store_true', help='Generate a detailed area report including surfing encounters')
    area_report_parser.add_argument('-o', '--other', action='store_true', help='Generate a detailed area report including other encounter types')
    area_report_parser.add_argument('-a', '--all', action='store_true', help='Generate a detailed area report including all encounter types')
    area_report_parser.add_argument('-C', '--companion-details', action='store_true', help='Include details for companion games in the report (if applicable)')
    area_report_parser.set_defaults(func=handle_area_report)

    pokemon_report_parser = subparsers.add_parser('pokemon-report', help='Generate a report for a specific Pokemon')
    pokemon_report_parser.add_argument('pokemon_name', type=str, help='Name of the Pokemon to generate report for')
    pokemon_report_parser.add_argument('-l', '--locations', action='store_true', help='Include location details in the report')
    pokemon_report_parser.set_defaults(func=handle_pokemon_report)

    completion_report_parser = subparsers.add_parser('completion', help='Generate a completion report for the tracked game')
    completion_report_parser.add_argument('-a', '--areas', action='store_true', help='Generate an area-by-area completion report')
    completion_report_parser.add_argument('-d', '--detailed', action='store_true', help='Generate a detailed completion report (caught, uncaught, and unavailable)')
    completion_report_parser.set_defaults(func=handle_completion_report)

    exclusives_parser = subparsers.add_parser('exclusives', help='Show which version exclusives from companion games are still needed for the tracked game')
    exclusives_parser.set_defaults(func=handle_exclusives)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)

if __name__ == "__main__":
    main()
