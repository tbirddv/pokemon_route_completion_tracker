from src.utils import format_list_for_output, get_terminal_width
from src.location import Location
from src.pokemon import Pokemon
from collections import deque

def create_progress_bar(current, total, width=40):
    width = int(width)
    if width < 10:
        return ""
    if total == 0:
        return "[No Pokemon in area]"
    
    percentage = current / total
    filled = int(width * percentage)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}]"



def filter_pokemon_list(pokemon_list, filter_list=None):
    if not filter_list:
        return pokemon_list
    return [p for p in pokemon_list if p in filter_list]

def format_pokemon_data(level_name: str, level_data: list, width: int, filter_list=None, indent_level=4):
    if not level_data:
        return ""
    filtered_data = filter_pokemon_list(level_data, filter_list)
    if filtered_data:
        if level_name.lower() != "main": #Default sublocation, no need to print it
            if indent_level + len(level_name + format_list_for_output(filtered_data, indent_level=1, max_width=width)) <= width: #check if it fits on one line
                            return " " * indent_level + f"{level_name}:" + format_list_for_output(filtered_data, indent_level=1, max_width=width) #Fits on one line
            else:
                return " " * indent_level + level_name + "\n" + format_list_for_output(filtered_data, indent_level=(indent_level + 2), max_width=width) #data_name on its own line, data indented
        else:
            return format_list_for_output(filtered_data, indent_level=indent_level, max_width=width) #data indented
    return ""

def handle_universal_area_params(area: Location, terminal_width=80):
    print("\nCaught:")
    if area.caught:
        print(format_list_for_output(list(sorted(area.caught)), indent_level=2, max_width=terminal_width))
    else:
        print("  None")
    if area.evolvable:
        print("\nEvolvable Pokemon (not caught, but can be evolved from another caught Pokemon):")
        formated_evolvable = format_list_for_output(list(sorted(area.evolvable)), indent_level=2, max_width=terminal_width)
        print(formated_evolvable)
    if area.devolvable:
        print("\nBreedable Pokemon (not caught, but can be obtained by breeding another caught Pokemon):")
        formated_devolvable = format_list_for_output(list(sorted(area.devolvable)), indent_level=2, max_width=terminal_width)
        print(formated_devolvable)

def build_simple_companion_report(remaining_unavailable_pokemon, encounter_summary_list, game_name):
    max_terminal_width = get_terminal_width(default=80)
    companion_game_pokemon_simple = set()
    for unavailable_pokemon in remaining_unavailable_pokemon:
        if unavailable_pokemon in encounter_summary_list:
            companion_game_pokemon_simple.add(unavailable_pokemon)
    if companion_game_pokemon_simple:
        single_line_string = f"  {game_name}:{format_list_for_output(list(sorted(companion_game_pokemon_simple)), indent_level=1, max_width=max_terminal_width)}"
        if len(single_line_string) <= max_terminal_width: #Try to fit on one line
            return single_line_string
         #If it doesn't fit on one line, try with a newline after the game name
        else:
            return f"  {game_name}:" + "\n" + format_list_for_output(list(sorted(companion_game_pokemon_simple)), indent_level=4, max_width=max_terminal_width)
    return ""

def build_tracking_sets(static_subtypes : set, **kwargs):
    tracked_encounter_types = set() #Set of encounter types being tracked based on input flags
    tracked_subtypes = static_subtypes.copy() #Set of encounter subtypes being tracked based on input flags, initialized with static subtypes that are always tracked
    if kwargs.get("walking", False):
        tracked_encounter_types.add("Walking")
    if kwargs.get("surfing", False):
        tracked_encounter_types.add("Surfing")
    if kwargs.get("super_rod", False):
        tracked_encounter_types.add("Fishing")
        tracked_subtypes.add("Super Rod")
    if kwargs.get("good_rod", False):
        tracked_encounter_types.add("Fishing")
        tracked_subtypes.add("Good Rod")
    if kwargs.get("old_rod", False):
        tracked_encounter_types.add("Fishing")
        tracked_subtypes.add("Old Rod")
    if kwargs.get("other", False):
        tracked_encounter_types.add("Other")
    
    if not tracked_encounter_types: #defensive only, should never happen due to CLI arg parsing
        tracked_encounter_types = {"Walking", "Surfing", "Fishing", "Other"}
        tracked_subtypes |= {"Super Rod", "Good Rod", "Old Rod"}

    return tracked_encounter_types, tracked_subtypes

def build_detailed_report_header(game_name, area_name, tracked_encounter_types, tracked_subtypes, static_subtypes):
    all_encounter_types = {"Walking", "Surfing", "Fishing", "Other"}
    all_trackable_subtypes = {"Super Rod", "Good Rod", "Old Rod"}
    max_terminal_width = get_terminal_width(default=80)
    if all_encounter_types == tracked_encounter_types and tracked_subtypes.issuperset(all_trackable_subtypes | static_subtypes): #All encounter types and subtypes being tracked
        header = f"\n--- Detailed Area Report for: {area_name} in Pokemon {game_name} (Tracking all encounter types) ---" 
    elif tracked_subtypes.issuperset(all_trackable_subtypes): #All tracked subtypes, but not all encounter types
        header = f"\n--- Detailed Area Report for: {area_name} in Pokemon {game_name} ---\n Tracking:{format_list_for_output([type for type in tracked_encounter_types], 1, max_width=max_terminal_width)}"
    else: #Some encounter types and subtypes being tracked
        header = f"\n--- Detailed Area Report for: {area_name} in Pokemon {game_name} ---\n Tracking:{format_list_for_output([type for type in tracked_encounter_types if type != 'Fishing'] + [subtype for subtype in tracked_subtypes if subtype not in static_subtypes], 1, max_width=max_terminal_width)}"
    return header

def process_sublocation_data(sublocation_name, sublocation_data, tracked_subtypes, width, filter_list=None):
    sublocation_lines = [] #Collect lines for this sublocation
    if isinstance(sublocation_data, list): #Walking and Surfing sublocations are mapped to lists of pokemon
        sublocation_report = format_pokemon_data(sublocation_name, sublocation_data, width, filter_list=filter_list, indent_level=4)
        if sublocation_report.strip():
            sublocation_lines.append(sublocation_report)

    elif isinstance(sublocation_data, dict): #Fishing and Other sublocations are mapped to dicts of subtypes to lists of pokemon
        subtype_lines = [] #Collect lines for each subtype within this sublocation
        for subtype, subtype_data in sublocation_data.items():
            if subtype not in tracked_subtypes: #tracked_subtypes is a set of subtypes we want to track
                continue
            if sublocation_name != "Main": #Main is the default sublocation, don't print it, indent subtypes less
                subtype_report = format_pokemon_data(subtype, subtype_data, width, filter_list=filter_list, indent_level=6)
            else:
                subtype_report = format_pokemon_data(subtype, subtype_data, width, filter_list=filter_list, indent_level=4)
            if subtype_report.strip():
                subtype_lines.append(subtype_report)
        if subtype_lines: #Only include this subtype if we found data for it
            if sublocation_name != "Main":
                sublocation_lines.append(f"    {sublocation_name}:")
            sublocation_lines.extend(subtype_lines)
    return sublocation_lines

def build_detailed_report_for_game(game_name: str, location: Location, tracked_encounter_types: set, tracked_subtypes: set, companion_version=False, filtered_pokemon_list=None):
    """
    This function builds a detailed report for a specific game and location.
    It takes into account the tracked encounter types and subtypes, and can filter the report based on a provided list of Pokemon names.
    If companion_version is True, the output format is adjusted for companion tracking mode.
    Args:
        game_name (str): The name of the game (e.g., "Red", "Blue", "Yellow"). For safety, use SupportedGames enum values.
        location (Location): The location object containing encounter data.
        tracked_types (set): A set of encounter types to include in the report (e.g., {"Walking", "Surfing"}).
        tracked_subtypes (set): A set of encounter subtypes to include in the report (e.g., {"Super Rod", "Good Rod"}).
        companion_version (bool): If True, formats output for companion tracking mode.
        filtered_pokemon_list (list or None): If provided, only includes Pokemon in this list.
    """
    max_terminal_width = get_terminal_width(default=80) #for formatting output nicely
    report_lines = deque() #Using deque for efficient appends and prepends
    for encounter_type in location.encounter_data[game_name]['uncaught']: #Iterate over encounter types in the location for the specified game
        encounter_lines = [] #Collect lines for this encounter type
        if encounter_type.lower() == 'all' or encounter_type not in tracked_encounter_types: #Detailed report, skip summary, also filter by tracked types
            continue
         #Collect lines for each sublocation within this encounter type
        for sublocation, sublocation_data in location.encounter_data[game_name]['uncaught'][encounter_type].items(): #Iterate over sublocations within the encounter type
            sublocation_report = process_sublocation_data(sublocation, sublocation_data, tracked_subtypes, max_terminal_width, filter_list=filtered_pokemon_list)

            if sublocation_report: #Only include this sublocation if we found data for it
                encounter_lines.extend(sublocation_report)

        if encounter_lines: #Only include this encounter type if we found data for it
            report_lines.append(f"  {encounter_type}:")
            report_lines.extend(encounter_lines)
    
    if report_lines: #If we found any data at all, prepend a header
        if not companion_version:
            report_lines.appendleft("\nUncaught Pokemon in this area:") #Header for tracked game
        else:
            report_lines.appendleft(game_name + ":") #Header for companion game
    if not report_lines: #If we found no data at all, print a message indicating that
        if not companion_version: #Only for the tracked game
            report_lines.append("No uncaught Pokemon found in this area for the selected encounter types.")
    return "\n".join(report_lines)

def completion_calcs(pokemon_list : list[Pokemon]):
    total = len(pokemon_list)
    caught = 0
    evolvable = 0
    devolvable = 0
    for pokemon in pokemon_list:
        if pokemon.status.lower() == "caught":
            caught += 1
        elif pokemon.status.lower() == "evolvable":
            evolvable += 1
        elif pokemon.status.lower() == "devolvable":
            devolvable += 1
    percent_caught = (caught / total * 100) if total > 0 else 0.0

    return total, caught, evolvable, devolvable, percent_caught

def build_completion_lists(save_data, companion_mode=False):
    caught = []
    uncaught = []
    evolvable = []
    devolvable = []
    unavailable = save_data.remaining_unavailable_pokemon if companion_mode else []
    for pokemon in save_data.pokemon:
        if pokemon.status.lower() == "caught":
            caught.append(pokemon)
        elif pokemon.status.lower() == "evolvable":
            evolvable.append(pokemon)
        elif pokemon.status.lower() == "devolvable":
            devolvable.append(pokemon)
        else:
            uncaught.append(pokemon)
        
    return caught, uncaught, evolvable, devolvable, unavailable
