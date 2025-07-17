from operator import sub
from src.utils import get_game_enum,  load_save_file, get_terminal_width, format_list_for_output, get_object_from_save, ObjectType
from Data.constants import SupportedGames, Generation_1, TRADE_EVOLUTIONS
from src.pokemon import Local_Gen1, Pokemon
from src.location import Gen1Location, Location
from src.report_utils import *


def simple_area_report(game_name, area_name, companion_mode=False):
    game = get_game_enum(game_name)
    save_data = load_save_file(game.value)
    area_name = area_name.strip().lower()
    terminal_width = get_terminal_width(default=80)

    found_area = None
    for location in save_data.locations:
        if location.name.lower() == area_name:
            found_area = location
            break

    if not found_area:
        print(f"Area {area_name} not found in save data for game {game.value}. Please ensure correct game is loaded and area name is accurate.")
        return
    
    print(f"\n--- Simple Area Report for: {found_area.name} in Pokemon {game.value} ---")
    handle_universal_area_params(found_area, terminal_width=terminal_width)
    uncaught = found_area.encounter_data[game.value]['uncaught']['All']
    if uncaught:
        print("\nUncaught Pokemon:")
        formated_uncaught = format_list_for_output(list(sorted(uncaught)), indent_level=2, max_width=terminal_width)
        print(formated_uncaught)
    if not uncaught:
        print("All Pokemon in this area have been caught!")
    if companion_mode:
        if not save_data.remaining_unavailable_pokemon:
            print("All Pokemon not found in this game have been caught!")
            return
        companion_reports = []
        for game_in_generation in found_area.encounter_data.keys():
            if game_in_generation != game.value:
                companion_game_location_summary = found_area.encounter_data[game_in_generation]['uncaught']['All']
                companion_report = build_simple_companion_report(save_data.remaining_unavailable_pokemon, companion_game_location_summary, game_in_generation)
                if companion_report.strip():
                    companion_reports.append(companion_report)
        if companion_reports:
            print("\nPokemon not found in this game that can be caught in this area in companion games:")
            print("\n".join(companion_reports))
        else:
            print("No Pokemon not found in this game can be caught in this area in companion games.")
    total_pokemon = len(found_area.encounter_data[game.value]['const']['All'])
    if total_pokemon != 0:
        filtered_caught = filter_pokemon_list(found_area.caught, found_area.encounter_data[game.value]['const']['All'])
        filtered_caught_count = len(filtered_caught)
        print(f"{create_progress_bar(filtered_caught_count, total_pokemon, width=get_terminal_width(default=80)/2)} {filtered_caught_count/total_pokemon*100:.2f}% Complete.")

def detailed_area_report(game_name, area_name, **kwargs):
    
    game = get_game_enum(game_name)
    save_data = load_save_file(game.value)
    area_name = area_name.strip().lower()
    static_subtypes = {"Gift", "Trade", "Buy", "Interact", "Revive", "uncaught"} #Static encounter subtypes always tracked
    tracked_encounter_types, tracked_subtypes = build_tracking_sets(**kwargs, static_subtypes=static_subtypes)

    found_area = get_object_from_save(save_data, area_name, ObjectType.LOCATION)

    if not found_area:
        print(f"Area {area_name} not found in save data for game {game.value}. Please ensure correct game is loaded and area name is accurate.")
        return
    
    print(build_detailed_report_header(game.value, found_area.name, tracked_encounter_types, tracked_subtypes, static_subtypes))
    print()
    handle_universal_area_params(found_area, terminal_width=get_terminal_width(default=80))
    
    if not found_area.encounter_data[game.value]["uncaught"]["All"]: #Do not have to check for presense in game as we traverse over tracked types
        print("All Pokemon in this area have been caught in this game!")
        
    else:
        report_text = build_detailed_report_for_game(game.value, found_area, tracked_encounter_types, tracked_subtypes, companion_version=False)
        print(report_text + "\n")

    if kwargs.get("companion_tracking", False):
        if not save_data.remaining_unavailable_pokemon:
            print("All Pokemon in this generation have been caught in your tracked game!")
            return
        companion_games_reports = []
        for game_in_generation in found_area.encounter_data.keys():
            if game_in_generation == game.value:
                continue

            companion_game_location_summary = found_area.encounter_data[game_in_generation]['uncaught']['All']
            if not companion_game_location_summary: #No uncaught pokemon in this area for this companion game
                continue

            if kwargs.get("companion_details", False): #Detailed companion report
                companion_game_report = build_detailed_report_for_game(game_in_generation, found_area, companion_game_location_summary, tracked_subtypes, companion_version=True, filtered_pokemon_list=save_data.remaining_unavailable_pokemon)
                if companion_game_report.strip():
                    companion_games_reports.append(companion_game_report)
            else:
                simple_companion_game_report = build_simple_companion_report(save_data.remaining_unavailable_pokemon, companion_game_location_summary, game_in_generation)
                if simple_companion_game_report.strip():
                    companion_games_reports.append(simple_companion_game_report)


        if companion_games_reports:
            print("Uncaught Pokemon not found in this game found in this area of other games in this generation:")
            print('\n'.join(companion_games_reports))
        else:
            print("No Pokemon not found in this game are found in this area in the other games in this generation.")
    filtered_caught = filter_pokemon_list(found_area.caught, found_area.encounter_data[game.value]['const']['All'])
    filtered_caught_count = len(filtered_caught)
    total_pokemon = len(found_area.encounter_data[game.value]['const']['All'])
    print(f"{create_progress_bar(filtered_caught_count, total_pokemon, width=get_terminal_width(default=80)/2)} {filtered_caught_count/total_pokemon*100:.2f}% Complete.")

def basic_individual_pokemon_report(game_name, pokemon_name, location=False, companions=False):
    game = get_game_enum(game_name)
    save_data = load_save_file(game.value)
    pokemon_name = pokemon_name.strip().lower()

    found_pokemon = get_object_from_save(save_data, pokemon_name, ObjectType.POKEMON)

    if not found_pokemon:
        print(f"Pokemon {pokemon_name} not found in save data for game {game.value}. Please ensure correct game is loaded and Pokemon name is accurate.")
        return
    
    print(f"\n--- Report for: #{found_pokemon.id} {found_pokemon.name.title()} in Pokemon {game.value} ---")
    print()
    print("Status:")
    if found_pokemon.status == "Evolvable":
        if found_pokemon.name in TRADE_EVOLUTIONS:
            print(f"{found_pokemon.name.title()} is not caught, but can be obtained by trading {found_pokemon.devolutions[-1].title()} with another player.")
        else:
            print(f"{found_pokemon.name.title()} is not caught, but can be evolved from {' -> '.join([p.title() for p in found_pokemon.devolutions])}.")
    elif found_pokemon.status == "Devolvable":
        print(f"{found_pokemon.name.title()} is not caught, but can be obtained by breeding {' or '.join([p.title() for p in found_pokemon.evolutions])}.")
    else:
        print(f"{found_pokemon.status}")
    print()
    if location:
        if found_pokemon.locations[game.value]:
            print(f"Locations {found_pokemon.name.title()} is found in the current game:\n")
            formated_locations = format_list_for_output([loc.title() for loc in sorted(found_pokemon.locations[game.value])], indent_level=2, max_width=get_terminal_width(default=80))
            print(formated_locations)
        else:
            print("Not found in any locations in current game.")
        print()
        if companions:
            print(f"Locations {found_pokemon.name.title()} is found in other games in this generation:")
            for game_in_gen, locs in found_pokemon.locations.items():
                if game_in_gen == game.value:
                    continue
                if locs:
                    print(format_pokemon_data(game_in_gen, [loc for loc in locs], get_terminal_width(default=80), indent_level=2))
                else:
                    print(f"  {game_in_gen}: Not found in any locations in this game.")


def simple_completion_report(game_name):
    game = get_game_enum(game_name)
    save_data = load_save_file(game.value)
    total_pokemon, caught_count, evolvable_count, breedable_count, percentage_complete = completion_calcs(save_data.pokemon)
    print(f"\n--- Simple Completion Report for Pokemon {game.value} ---\n")
    print(f"Total Pokemon: {total_pokemon}")
    print(f"Caught Pokemon: {caught_count}")
    if evolvable_count > 0:
        print(f"Evolvable Pokemon (not caught, but can be evolved from another caught Pokemon): {evolvable_count}")
    if breedable_count > 0:
        print(f"Breedable Pokemon (not caught, but can be obtained by breeding another caught Pokemon): {breedable_count}")
    print(f"Uncaught Pokemon: {total_pokemon - caught_count}")
    print(create_progress_bar(caught_count, total_pokemon, width=get_terminal_width(default=80)/2))
    print(f"Your Pokedex is {percentage_complete:.2f}% complete.")

def detailed_completion_report(game_name, companion=False):
    game = get_game_enum(game_name)
    save_data = load_save_file(game.value)
    print(f"\n--- Detailed Completion Report for Pokemon {game.value} ---\n")
    terminal_width = get_terminal_width(default=80)

    caught_pokemon, uncaught_pokemon, evolvable_pokemon, breedable_pokemon, unavailable_pokemon = build_completion_lists(save_data, companion_mode=companion)

    total_pokemon = len(save_data.pokemon)
    caught_count = len(caught_pokemon)
    uncaught_count = total_pokemon - caught_count

    print(f"Total Pokemon: {total_pokemon}")
    print(f"Caught Pokemon: {caught_count}")
    print(f"Uncaught Pokemon: {uncaught_count}")
    print(create_progress_bar(caught_count, total_pokemon, width=terminal_width/2))
    print(f"Your Pokedex is {caught_count / total_pokemon * 100:.2f}% complete.")
    print()
    print("Caught Pokemon:")
    if caught_pokemon:
        formated_caught = format_list_for_output([mon.name for mon in sorted(caught_pokemon, key=lambda p: p.national_id)], indent_level=2, max_width=terminal_width)
        print(formated_caught)
    else:
        print("  None")
    print()
    if uncaught_pokemon:
        print("Uncaught Pokemon:")
        formated_uncaught = format_list_for_output([mon.name for mon in sorted(uncaught_pokemon, key=lambda p: p.national_id)], indent_level=2, max_width=terminal_width)
        print(formated_uncaught)
    else:
        print("All Pokemon have been caught! Congratulations!")
    print()
    if evolvable_pokemon:
        print("Evolvable Pokemon (not caught, but can be evolved from another caught Pokemon):")
        formated_evolvable = format_list_for_output([mon.name for mon in sorted(evolvable_pokemon, key=lambda p: p.national_id)], indent_level=2, max_width=terminal_width)
        print(formated_evolvable)
        print()
    if breedable_pokemon:
        print("Breedable Pokemon (not caught, but can be obtained by breeding another caught Pokemon):")
        formated_breedable = format_list_for_output([mon.name for mon in sorted(breedable_pokemon, key=lambda p: p.national_id)], indent_level=2, max_width=terminal_width)
        print(formated_breedable)
        print()
    if unavailable_pokemon:
        print("Uncaught pokemon not available in this game (e.g., version exclusives, event-only):")
        formated_unavailable = format_list_for_output([unavailable.title() for unavailable in unavailable_pokemon], indent_level=2, max_width=terminal_width)
        print(formated_unavailable)
    print()

def show_remaining_exclusives(game_name):
    game = get_game_enum(game_name)
    save_data = load_save_file(game.value)

    if not save_data.remaining_unavailable_pokemon:
        print("All version exclusive and event pokemon have been caught!")
        return
    
    print(f"Remaining version exclusive and event pokemon not caught in Pokemon {game.value}:")
    terminal_width = get_terminal_width(default=80)
    formated_unavailable = format_list_for_output(save_data.remaining_unavailable_pokemon, indent_level=2, max_width=terminal_width)
    print(formated_unavailable)

def build_completion_report_by_area(game_name, detailed=False):
    game = get_game_enum(game_name)
    save_data = load_save_file(game.value)
    terminal_width = get_terminal_width(default=80)
    if detailed:
        print(f"--- Detailed Completion Report by Area for Pokemon {game.value} ---\n")
    else:
        print(f"--- Simple Completion Report by Area for Pokemon {game.value} ---\n")
    for location in save_data.locations:
        caught = location.caught
        total = location.encounter_data[game.value]['const']['All']
        version_filtered_caught = filter_pokemon_list(caught, total)
        caught_count = len(version_filtered_caught)
        total_count = len(total)
        percentage_complete = (caught_count / total_count * 100) if total_count > 0 else 0
        status = f"{caught_count}/{total_count} ({percentage_complete:.2f}% complete)" if total_count > 0 else "N/A"
        if not detailed:
            print(f"{create_progress_bar(caught_count, total_count, width=terminal_width/4)} {location.name}: {status}")
        else:
            print(f"{location.name}:")
            print(create_progress_bar(caught_count, total_count, width=terminal_width/2))
            if not version_filtered_caught:
                print("  Caught: None")
            else:
                print(format_pokemon_data("Caught", version_filtered_caught, terminal_width, indent_level=2))
            if not location.encounter_data[game.value]['uncaught']['All']:
                print("  Uncaught: None")
            else:
                print(format_pokemon_data("Uncaught", location.encounter_data[game.value]['uncaught']['All'], terminal_width, indent_level=2))
            print(f"  Completion: {status}\n")
    print("\nOverall Completion:")
    total_pokemon, caught_count, evolvable_count, breedable_count, percentage_complete = completion_calcs(save_data.pokemon)
    print(create_progress_bar(caught_count, total_pokemon, width=terminal_width/2))
    print(f"Your Pokedex is {percentage_complete:.2f}% complete. ({caught_count}/{total_pokemon} caught)")

def items_needed_for_area_report(game_name, area_name):
    game = get_game_enum(game_name)
    save_data = load_save_file(game.value)
    area_name = area_name.strip().lower()

    found_area = get_object_from_save(save_data, area_name, ObjectType.LOCATION)

    if not found_area:
        print(f"Area {area_name} not found in save data for game {game.value}. Please ensure correct game is loaded and area name is accurate.")
        return
    
    area_const_data = found_area.encounter_data.get(game.value, {}).get('const', {})

    items_had = []
    items_needed = []

    if area_const_data.get('Surfing', {}):
        if save_data.settings.surf:
            items_had.append('HM Surf')
        else:
            items_needed.append('HM Surf')

    if area_const_data.get('Fishing', {}):
        for rod_type in ['Old Rod', 'Good Rod', 'Super Rod']:
            if area_const_data['Fishing'].get(rod_type, []):
                if getattr(save_data.settings, rod_type.replace(" ", "_").lower()):
                    items_had.append(rod_type)
                else:
                    items_needed.append(rod_type)

    print()
    print(f"Items needed to catch all Pokemon in {found_area.name} in Pokemon {game.value}:")
    if items_had:
        print("\nAlready Have:")
        print(f"  {', '.join(items_had)}")
    if items_needed:
        print("\nStill Needed:")
        print(f"  {', '.join(items_needed)}")
    if not items_had and not items_needed:
        print("No items are needed for this area.")
    print()

