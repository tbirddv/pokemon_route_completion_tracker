from src.utils import (get_game_enum, SaveData, save_game_data, load_save_file)
from Data.constants import SupportedGames, Generation_1
from src.pokemon import Local_Gen1, Pokemon
from src.location import Gen1Location, Location

def simple_area_report(game_name, area_name):
    game = get_game_enum(game_name)
    save_data = load_save_file(game.value)
    area_name = area_name.strip().lower()

    found_area = None
    for location in save_data.locations:
        if location.name.lower() == area_name:
            found_area = location
            break

    if not found_area:
        print(f"Area {area_name} not found in save data for game {game.value}. Please ensure correct game is loaded and area name is accurate.")
        return
    
    print(f"\n--- Simple Area Report for: {found_area.name} in Pokemon {game.value} ---")
    print(f"Caught Pokemon: {', '.join(sorted([p.title() for p in found_area.caught])) if found_area.caught else 'None'}")
    uncaught = found_area.uncaught_fields()[game]['All']
    print(f"Uncaught Pokemon: {', '.join(sorted([p.title() for p in uncaught]) if uncaught else 'None')}")
    if not uncaught:
        print("All Pokemon in this area have been caught!")
    else:
        if save_data.remaining_unavailable_pokemon:
            for game_in_gen in found_area.uncaught_fields().keys():
                if game_in_gen == game:
                    continue
                companion_game_uncaught = []
                if found_area.uncaught_fields()[game_in_gen]['All']:
                    for pokemon in save_data.remaining_unavailable_pokemon:
                        if pokemon in found_area.uncaught_fields()[game_in_gen]['All']:
                            companion_game_uncaught.append(pokemon)
                if companion_game_uncaught:
                    print(f"Uncaught Pokemon unavailable in this game found in this area of Pokemon {game_in_gen.value}: {', '.join(sorted(companion_game_uncaught))}")

def build_detailed_report_for_game(game, game_specific_uncaught_fields, tracking_types: set, companion_version=False, filtered_pokemon_list=None): #all is default state, removed kwarg
    """
    This is designed to contain most of the logic for building a detailed report for a specific game in an area.
    Since different outputs are expected for tracked game vs companion games, the companion_version flag is used to adjust output formatting and verbosity.
    
    Args:
        game_specific_uncaught_fields (dict): The uncaught fields for a specific game in an area.
        tracking_types (set): Set of encounter types being tracked (e.g., Walking, Surfing, Fishing, Other).
        companion_version (bool): Whether this report is for a companion game (less verbose).
        filtered_pokemon_list (list, optional): For companion games, only include these pokemon if provided. If None, include all uncaught pokemon.
    Returns:
        str: The formatted report string. 
    """

    report_lines = []
    encounter_blocks = [] #List of strings for each encounter type block to be joined later, separate from report_lines due to verbosity differences

    for encounter_type_name, encounter_type_data in game_specific_uncaught_fields.items():
        if encounter_type_name.lower() == "all": #Skip the all field, we want to break down by encounter type
            continue

        if encounter_type_name not in tracking_types: #Skip encounter types not being tracked
            continue

        if isinstance(encounter_type_data, dict): #This should always be true since encounter types are always dicts of sublocations
            sublocation_output_blocks = []
            for sublocation_name, sublocation_data in encounter_type_data.items():
                sublocation_string = f"      {sublocation_name}: " if sublocation_name.lower() != "main" else "      " #We always want some indenting, but no sublocation name for main, always used can be defined here

                if isinstance(sublocation_data, list): #This should be walking/surfing encounters
                    if sublocation_data: #Skips empty lists
                        if filtered_pokemon_list is not None: #Companion game with filtered pokemon list
                            filtered_sublocation_data = [p for p in sublocation_data if p in filtered_pokemon_list]
                            if filtered_sublocation_data:
                                sublocation_output_blocks.append(sublocation_string + ", ".join([p.title() for p in sorted(filtered_sublocation_data)]))
                        else: #Tracked game or companion game with no filtered list, include all pokemon
                            sublocation_output_blocks.append(sublocation_string + ", ".join([p.title() for p in sorted(sublocation_data)]))

                    elif isinstance(sublocation_data, dict): #This should be fishing/other encounters with subtypes
                        subtype_lines = []
                        for subtype_name, subtype_data in sublocation_data.items():
                            if subtype_data: #Only print subtypes with data
                                if filtered_pokemon_list is not None: #Companion game with filtered pokemon list
                                    filtered_subtype_data = [p for p in subtype_data if p in filtered_pokemon_list]
                                    if filtered_subtype_data:
                                        subtype_lines.append(f"        {subtype_name}: {', '.join([p.title() for p in sorted(filtered_subtype_data)])}")
                                else: #Tracked game or companion game with no filtered list, include all pokemon
                                    subtype_lines.append(f"        {subtype_name}: {', '.join([p.title() for p in sorted(subtype_data)])}")
                        if subtype_lines:
                            sublocation_output_blocks.append(sublocation_string + "\n" + "\n".join(subtype_lines))

            if sublocation_output_blocks: #No need for additional check since it is only populated if there is data to show
                encounter_blocks.append(f"  {encounter_type_name}:\n" + "\n  ".join(sublocation_output_blocks))
            
            
        elif isinstance(encounter_type_data, list): #This should never happen just here for safety, encounter types should always be dicts of sublocations
            if encounter_type_name in tracking_types or "All" in tracking_types:
                if encounter_type_data:
                    if filtered_pokemon_list is not None: #Companion game with filtered pokemon list
                        filtered_encounter_data = [p for p in encounter_type_data if p in filtered_pokemon_list]
                        if filtered_encounter_data:
                            encounter_blocks.append(f"    {encounter_type_name}:\n      " + ", ".join(sorted([p.title() for p in filtered_encounter_data])))
                    else: #Tracked game or companion game with no filtered list, include all pokemon
                        encounter_blocks.append(f"  {encounter_type_name}:\n      " + ", ".join(sorted([p.title() for p in encounter_type_data])))
    if encounter_blocks: #Again will only be populated if there is data to show
        if not companion_version:
            report_lines.append("\nUncaught Pokemon in this area:")
        if companion_version:
            report_lines.append(game.value + ":")
        report_lines.extend(encounter_blocks)

        

    else:
        if not companion_version:
            report_lines.append("No uncaught Pokemon found in this area for the selected encounter types.")

    return "\n".join(report_lines)


def detailed_area_report(game_name, area_name, walking=False, surfing=False, fishing=False, other=False, unavailable=False, companion_details=False):
    tracking_types = set() #Set of encounter types being tracked based on input flags
    if walking:
        tracking_types.add("Walking")
    if surfing:
        tracking_types.add("Surfing")
    if fishing:
        tracking_types.add("Fishing")
    if other:
        tracking_types.add("Other")
    if not tracking_types: #defensive only, should never happen due to CLI arg parsing
        tracking_types = {"Walking", "Surfing", "Fishing", "Other"}
    game = get_game_enum(game_name)
    save_data = load_save_file(game.value)
    area_name = area_name.strip().lower()
    
    found_area = None
    for location in save_data.locations:
        if location.name.lower() == area_name:
            found_area = location
            break

    if not found_area:
        print(f"Area {area_name} not found in save data for game {game.value}. Please ensure correct game is loaded and area name is accurate.")
        return
    
    if isinstance(found_area, Location):
        if tracking_types == {"Walking", "Surfing", "Fishing", "Other"}:
            print(f"\n--- Detailed Area Report for: {found_area.name} in Pokemon {game.value} (Tracking all encounter types) ---")
        else:
            print(f"\n--- Detailed Area Report for: {found_area.name} in Pokemon {game.value} (Tracking encounter types: {', '.join(sorted(tracking_types))}) ---")
        print("\nCaught Pokemon:")
        if found_area.caught:
            print(f"  {', '.join(sorted([p.title() for p in found_area.caught]))}")
        else:
            print("  None")
        print()
        uncaught_fields_data = found_area.uncaught_fields()
        if not uncaught_fields_data[game]["All"]: #Do not have to check for presense in game as we traverse over tracked types
            print("All Pokemon in this area have been caught in this game!")
        
        else:
            report_text = build_detailed_report_for_game(game, uncaught_fields_data[game], tracking_types=tracking_types)
            print(report_text)
            print() #Extra newline for spacing

        if unavailable:
            if save_data.remaining_unavailable_pokemon:
                companion_games_uncaught_pokemon = []
                for game_in_generation in uncaught_fields_data.keys():
                    if game_in_generation == game:
                        continue
                    companion_game_name = game_in_generation.value
                    companion_game_uncaught_fields = uncaught_fields_data[game_in_generation]

                    if not companion_game_uncaught_fields['All']: #No uncaught pokemon in this area for this companion game
                        continue
                    
                    if not companion_details:
                        companion_game_pokemon_simple = set()
                        for unavailable_pokemon in save_data.remaining_unavailable_pokemon:
                            if unavailable_pokemon in companion_game_uncaught_fields['All']:
                                companion_game_pokemon_simple.add(unavailable_pokemon)
                        if companion_game_pokemon_simple:
                            companion_games_uncaught_pokemon.append(f"  {companion_game_name}: {', '.join(sorted([p.title() for p in companion_game_pokemon_simple]))}")
                        continue
                    #Detailed companion game report with encounter types and location once I figure out a good way to do that will go here
                    companion_game_detailed_report = build_detailed_report_for_game(game_in_generation, companion_game_uncaught_fields, tracking_types=tracking_types, companion_version=True, filtered_pokemon_list=save_data.remaining_unavailable_pokemon)
                    if companion_game_detailed_report.strip():
                        companion_games_uncaught_pokemon.append(f"\n{companion_game_detailed_report}")

                if companion_games_uncaught_pokemon:
                    print("Uncaught Pokemon unavailable in this game found in this area of companion games:")
                    print('\n'.join(companion_games_uncaught_pokemon))
                else:
                    print("No unavailable uncaught Pokemon found in this area in companion games.")
            else:
                print("All pokemon unavailable in this game have been caught!")


def basic_individual_pokemon_report(game_name, pokemon_name, location=False, companions=False):
    game = get_game_enum(game_name)
    save_data = load_save_file(game.value)
    pokemon_name = pokemon_name.strip().lower()

    found_pokemon = None
    for pokemon in save_data.pokemon:
        if pokemon.name == pokemon_name:
            found_pokemon = pokemon
            break

    if not found_pokemon:
        print(f"Pokemon {pokemon_name} not found in save data for game {game.value}. Please ensure correct game is loaded and Pokemon name is accurate.")
        return
    
    print(f"\n--- Basic Report for: #{found_pokemon.id} {found_pokemon.name.title()} in Pokemon {game.value} ---")
    print()
    print(f"Status: {found_pokemon.status}")
    print()
    if location:
        locations_fields = found_pokemon.locations_fields()
        if locations_fields[game]:
            print(f"Locations in current game: {', '.join(sorted([loc.title() for loc in locations_fields[game]]))}")
        else:
            print("Not found in any locations in current game.")
    print()
    if companions:
        print("Locations in companion games:")
        for game_in_gen, locs in locations_fields.items():
            if game_in_gen == game:
                continue
            if locs:
                print(f"  {game_in_gen.value}: {', '.join(sorted([loc.title() for loc in locs]))}")
            else:
                print(f"  {game_in_gen.value}: Not found in any locations in this game.")
