import copy
from enum import Enum
from Data.constants import SupportedGames

class ModificationType(Enum):
    CATCH = 'catch'
    EVOLVABLE = 'evolvable'
    DEVOLVABLE = 'devolvable'
    EVOLVE = 'evolve'
    DEVOLVE = 'devolve'

class Location:
    def __init__(self, name, caught = None, evolvable = None, devolvable = None):
        self.name = name
        self.caught = set(caught) if caught is not None else set()
        self.evolvable = set(evolvable) if evolvable is not None else set()
        self.devolvable = set(devolvable) if devolvable is not None else set()

    def to_dict(self):
        return {
            'name': self.name,
            'caught': list(self.caught),
            'evolvable': list(self.evolvable),
            'devolvable': list(self.devolvable)
        }

class Gen1Location(Location):
    def __init__(self, name, red_all_const, red_all_uncaught,
                 red_walking_const, red_walking_uncaught,
                 red_surfing_const, red_surfing_uncaught,
                 red_fishing_const, red_fishing_uncaught,
                 red_other_const, red_other_uncaught,
                 blue_all_const, blue_all_uncaught, 
                 blue_walking_const, blue_walking_uncaught,
                 blue_surfing_const, blue_surfing_uncaught,
                 blue_fishing_const, blue_fishing_uncaught,
                 blue_other_const, blue_other_uncaught,
                 yellow_all_const, yellow_all_uncaught,
                 yellow_walking_const, yellow_walking_uncaught,
                 yellow_surfing_const, yellow_surfing_uncaught,
                 yellow_fishing_const, yellow_fishing_uncaught,
                 yellow_other_const, yellow_other_uncaught,
                 caught = None, evolvable = None, devolvable = None):
        super().__init__(name, caught, evolvable, devolvable)
        self.red_all_const = red_all_const
        self.red_all_uncaught = red_all_uncaught
        self.red_walking_const = red_walking_const
        self.red_walking_uncaught = red_walking_uncaught
        self.red_surfing_const = red_surfing_const
        self.red_surfing_uncaught = red_surfing_uncaught
        self.red_fishing_const = red_fishing_const
        self.red_fishing_uncaught = red_fishing_uncaught
        self.red_other_const = red_other_const
        self.red_other_uncaught = red_other_uncaught
        self.blue_all_const = blue_all_const
        self.blue_all_uncaught = blue_all_uncaught
        self.blue_walking_const = blue_walking_const
        self.blue_walking_uncaught = blue_walking_uncaught
        self.blue_surfing_const = blue_surfing_const
        self.blue_surfing_uncaught = blue_surfing_uncaught
        self.blue_fishing_const = blue_fishing_const
        self.blue_fishing_uncaught = blue_fishing_uncaught
        self.blue_other_const = blue_other_const
        self.blue_other_uncaught = blue_other_uncaught
        self.yellow_all_const = yellow_all_const
        self.yellow_all_uncaught = yellow_all_uncaught
        self.yellow_walking_const = yellow_walking_const
        self.yellow_walking_uncaught = yellow_walking_uncaught
        self.yellow_surfing_const = yellow_surfing_const
        self.yellow_surfing_uncaught = yellow_surfing_uncaught
        self.yellow_fishing_const = yellow_fishing_const
        self.yellow_fishing_uncaught = yellow_fishing_uncaught
        self.yellow_other_const = yellow_other_const
        self.yellow_other_uncaught = yellow_other_uncaught
    
    @classmethod
    def from_csv(cls, row):
        name = row['Area Name']
        red_all_const = set()
        red_walking_const = {subloc.strip(): [mon.strip().lower() for mon in pokemon.strip().split('/') if mon.strip() != '' and mon.strip().lower() != "none"]
                             for subloc, pokemon in (sublocation.strip().split(':') for sublocation in row['Red Walking'].strip().split(';') if sublocation.strip() != '' and sublocation.strip().lower() != "none" and len(sublocation.split(':')) == 2)
                               if subloc.strip() != '' and subloc.strip().lower() != "none" and pokemon.strip() != '' and pokemon.strip().lower() != "none"}
        for pokemon_list in red_walking_const.values():
            red_all_const.update(pokemon_list)
        red_walking_uncaught = copy.deepcopy(red_walking_const)
        red_surfing_const = {subloc.strip(): [mon.strip().lower() for mon in pokemon.strip().split('/') if mon.strip() != '' and mon.strip().lower() != "none"]
                             for subloc, pokemon in (sublocation.strip().split(':') for sublocation in row['Red Surfing'].strip().split(';') if sublocation.strip() != '' and sublocation.strip().lower() != "none" and len(sublocation.split(':')) == 2)
                               if subloc.strip() != '' and subloc.strip().lower() != "none" and pokemon.strip() != '' and pokemon.strip().lower() != "none"}
        for pokemon_list in red_surfing_const.values():
            red_all_const.update(pokemon_list)
        red_surfing_uncaught = copy.deepcopy(red_surfing_const)
        red_fishing_const = {}
        if row['Red Fishing'].strip() != '' and row['Red Fishing'].strip().lower() != "none":
            fishing_sublocations = row['Red Fishing'].strip().split(';')
            for sublocation in fishing_sublocations:
                sublocation = sublocation.strip()
                if sublocation.lower() != "none" and sublocation != '':
                    parts = sublocation.split('~')
                    if parts and len(parts) > 1:
                        subloc_name = parts[0].strip()
                        if subloc_name.lower() != "none" and subloc_name != '':
                            subtypes = [part.strip() for part in parts[1:] if part.strip() != '' and part.strip().lower() != "none"]
                            red_fishing_const[subloc_name] = {subtype.split(':')[0].strip(): [pokemon.strip().lower() for pokemon in subtype.split(':')[1].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
                                                             for subtype in subtypes if ':' in subtype and len(subtype.split(':')) == 2 and subtype.split(':')[1].strip() != '' and subtype.split(':')[1].strip().lower() != "none"}
        for sublocation in red_fishing_const.keys():
            for pokemon_list in red_fishing_const[sublocation].values():
                red_all_const.update(pokemon_list)
        red_fishing_uncaught = copy.deepcopy(red_fishing_const)
        red_other_const = {}
        if row['Red Other'].strip() != '' and row['Red Other'].strip().lower() != "none":
            other_sublocations = row['Red Other'].strip().split(';')
            for sublocation in other_sublocations:
                sublocation = sublocation.strip()
                if sublocation.lower() != "none" and sublocation != '':
                    parts = sublocation.split('~')
                    if parts and len(parts) > 1:
                        subloc_name = parts[0].strip()
                        if subloc_name.lower() != "none" and subloc_name != '':
                            subtypes = [part.strip() for part in parts[1:] if part.strip() != '' and part.strip().lower() != "none"]
                            red_other_const[subloc_name] = {subtype.split(':')[0].strip(): [pokemon.strip().lower() for pokemon in subtype.split(':')[1].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
                                                             for subtype in subtypes if ':' in subtype and len(subtype.split(':')) == 2 and subtype.split(':')[1].strip() != '' and subtype.split(':')[1].strip().lower() != "none"}
        for sublocation in red_other_const.keys():
            for pokemon_list in red_other_const[sublocation].values():
                red_all_const.update(pokemon_list)
        red_other_uncaught = copy.deepcopy(red_other_const)
        red_all_uncaught = red_all_const.copy()
        blue_all_const = set()
        blue_walking_const = {subloc.strip(): [mon.strip().lower() for mon in pokemon.strip().split('/') if mon.strip() != '' and mon.strip().lower() != "none"]
                             for subloc, pokemon in (sublocation.strip().split(':') for sublocation in row['Blue Walking'].strip().split(';') if sublocation.strip() != '' and sublocation.strip().lower() != "none" and len(sublocation.split(':')) == 2)
                               if subloc.strip() != '' and subloc.strip().lower() != "none" and pokemon.strip() != '' and pokemon.strip().lower() != "none"}
        for pokemon_list in blue_walking_const.values():
            blue_all_const.update(pokemon_list)
        blue_walking_uncaught = copy.deepcopy(blue_walking_const)
        blue_surfing_const = {subloc.strip(): [mon.strip().lower() for mon in pokemon.strip().split('/') if mon.strip() != '' and mon.strip().lower() != "none"]
                             for subloc, pokemon in (sublocation.strip().split(':') for sublocation in row['Blue Surfing'].strip().split(';') if sublocation.strip() != '' and sublocation.strip().lower() != "none" and len(sublocation.split(':')) == 2)
                               if subloc.strip() != '' and subloc.strip().lower() != "none" and pokemon.strip() != '' and pokemon.strip().lower() != "none"}
        for pokemon_list in blue_surfing_const.values():
            blue_all_const.update(pokemon_list)
        blue_surfing_uncaught = copy.deepcopy(blue_surfing_const)
        blue_fishing_const = {}
        if row['Blue Fishing'].strip() != '' and row['Blue Fishing'].strip().lower() != "none":
            fishing_sublocations = row['Blue Fishing'].strip().split(';')
            for sublocation in fishing_sublocations:
                sublocation = sublocation.strip()
                if sublocation.lower() != "none" and sublocation != '':
                    parts = sublocation.split('~')
                    if parts and len(parts) > 1:
                        subloc_name = parts[0].strip()
                        if subloc_name.lower() != "none" and subloc_name != '':
                            subtypes = [part.strip() for part in parts[1:] if part.strip() != '' and part.strip().lower() != "none"]
                            blue_fishing_const[subloc_name] = {subtype.split(':')[0].strip(): [pokemon.strip().lower() for pokemon in subtype.split(':')[1].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
                                                             for subtype in subtypes if ':' in subtype and len(subtype.split(':')) == 2 and subtype.split(':')[1].strip() != '' and subtype.split(':')[1].strip().lower() != "none"}
        for sublocation in blue_fishing_const.keys():
            for pokemon_list in blue_fishing_const[sublocation].values():
                blue_all_const.update(pokemon_list)
        blue_fishing_uncaught = copy.deepcopy(blue_fishing_const)
        blue_other_const = {}
        if row['Blue Other'].strip() != '' and row['Blue Other'].strip().lower() != "none":
            other_sublocations = row['Blue Other'].strip().split(';')
            for sublocation in other_sublocations:
                sublocation = sublocation.strip()
                if sublocation.lower() != "none" and sublocation != '':
                    parts = sublocation.split('~')
                    if parts and len(parts) > 1:
                        subloc_name = parts[0].strip()
                        if subloc_name.lower() != "none" and subloc_name != '':
                            subtypes = [part.strip() for part in parts[1:] if part.strip() != '' and part.strip().lower() != "none"]
                            blue_other_const[subloc_name] = {subtype.split(':')[0].strip(): [pokemon.strip().lower() for pokemon in subtype.split(':')[1].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
                                                             for subtype in subtypes if ':' in subtype and len(subtype.split(':')) == 2 and subtype.split(':')[1].strip() != '' and subtype.split(':')[1].strip().lower() != "none"}
        for sublocation in blue_other_const.keys():
            for pokemon_list in blue_other_const[sublocation].values():
                blue_all_const.update(pokemon_list)
        blue_other_uncaught = copy.deepcopy(blue_other_const)
        blue_all_uncaught = blue_all_const.copy()
        yellow_all_const = set()
        yellow_walking_const = {subloc.strip(): [mon.strip().lower() for mon in pokemon.strip().split('/') if mon.strip() != '' and mon.strip().lower() != "none"]
                             for subloc, pokemon in (sublocation.strip().split(':') for sublocation in row['Yellow Walking'].strip().split(';') if sublocation.strip() != '' and sublocation.strip().lower() != "none" and len(sublocation.split(':')) == 2)
                               if subloc.strip() != '' and subloc.strip().lower() != "none" and pokemon.strip() != '' and pokemon.strip().lower() != "none"}
        for pokemon_list in yellow_walking_const.values():
            yellow_all_const.update(pokemon_list)
        yellow_walking_uncaught = copy.deepcopy(yellow_walking_const)
        yellow_surfing_const = {subloc.strip(): [mon.strip().lower() for mon in pokemon.strip().split('/') if mon.strip() != '' and mon.strip().lower() != "none"]
                             for subloc, pokemon in (sublocation.strip().split(':') for sublocation in row['Yellow Surfing'].strip().split(';') if sublocation.strip() != '' and sublocation.strip().lower() != "none" and len(sublocation.split(':')) == 2)
                               if subloc.strip() != '' and subloc.strip().lower() != "none" and pokemon.strip() != '' and pokemon.strip().lower() != "none"}
        for pokemon_list in yellow_surfing_const.values():
            yellow_all_const.update(pokemon_list)
        yellow_surfing_uncaught = copy.deepcopy(yellow_surfing_const)
        yellow_fishing_const = {}
        if row['Yellow Fishing'].strip() != '' and row['Yellow Fishing'].strip().lower() != "none":
            fishing_sublocations = row['Yellow Fishing'].strip().split(';')
            for sublocation in fishing_sublocations:
                sublocation = sublocation.strip()
                if sublocation.lower() != "none" and sublocation != '':
                    parts = sublocation.split('~')
                    if parts and len(parts) > 1:
                        subloc_name = parts[0].strip()
                        if subloc_name.lower() != "none" and subloc_name != '':
                            subtypes = [part.strip() for part in parts[1:] if part.strip() != '' and part.strip().lower() != "none"]
                            yellow_fishing_const[subloc_name] = {subtype.split(':')[0].strip(): [pokemon.strip().lower() for pokemon in subtype.split(':')[1].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
                                                             for subtype in subtypes if ':' in subtype and len(subtype.split(':')) == 2 and subtype.split(':')[1].strip() != '' and subtype.split(':')[1].strip().lower() != "none"}
        for sublocation in yellow_fishing_const.keys():
            for pokemon_list in yellow_fishing_const[sublocation].values():
                yellow_all_const.update(pokemon_list)
        yellow_fishing_uncaught = copy.deepcopy(yellow_fishing_const)
        yellow_other_const = {}
        if row['Yellow Other'].strip() != '' and row['Yellow Other'].strip().lower() != "none":
            other_sublocations = row['Yellow Other'].strip().split(';')
            for sublocation in other_sublocations:
                sublocation = sublocation.strip()
                if sublocation.lower() != "none" and sublocation != '':
                    parts = sublocation.split('~')
                    if parts and len(parts) > 1:
                        subloc_name = parts[0].strip()
                        if subloc_name.lower() != "none" and subloc_name != '':
                            subtypes = [part.strip() for part in parts[1:] if part.strip() != '' and part.strip().lower() != "none"]
                            yellow_other_const[subloc_name] = {subtype.split(':')[0].strip(): [pokemon.strip().lower() for pokemon in subtype.split(':')[1].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
                                                             for subtype in subtypes if ':' in subtype and len(subtype.split(':')) == 2 and subtype.split(':')[1].strip() != '' and subtype.split(':')[1].strip().lower() != "none"}
        for sublocation in yellow_other_const.keys():
            for pokemon_list in yellow_other_const[sublocation].values():
                yellow_all_const.update(pokemon_list)
        yellow_other_uncaught = copy.deepcopy(yellow_other_const)
        yellow_all_uncaught = yellow_all_const.copy()
        return cls(name, list(red_all_const), list(red_all_uncaught),
                   red_walking_const, red_walking_uncaught,
                   red_surfing_const, red_surfing_uncaught,
                   red_fishing_const, red_fishing_uncaught,
                   red_other_const, red_other_uncaught,
                   list(blue_all_const), list(blue_all_uncaught),
                   blue_walking_const, blue_walking_uncaught,
                   blue_surfing_const, blue_surfing_uncaught,
                   blue_fishing_const, blue_fishing_uncaught,
                   blue_other_const, blue_other_uncaught,
                   list(yellow_all_const), list(yellow_all_uncaught),
                   yellow_walking_const, yellow_walking_uncaught,
                   yellow_surfing_const, yellow_surfing_uncaught,
                   yellow_fishing_const, yellow_fishing_uncaught,
                   yellow_other_const, yellow_other_uncaught)
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            red_all_const=data.get('red_all_const', []),
            red_all_uncaught=data.get('red_all_uncaught', []),
            red_walking_const=data.get('red_walking_const', {}),
            red_walking_uncaught=data.get('red_walking_uncaught', {}),
            red_surfing_const=data.get('red_surfing_const', {}),
            red_surfing_uncaught=data.get('red_surfing_uncaught', {}),
            red_fishing_const=data.get('red_fishing_const', {}),
            red_fishing_uncaught=data.get('red_fishing_uncaught', {}),
            red_other_const=data.get('red_other_const', {}),
            red_other_uncaught=data.get('red_other_uncaught', {}),
            blue_all_const=data.get('blue_all_const', []),
            blue_all_uncaught=data.get('blue_all_uncaught', []),
            blue_walking_const=data.get('blue_walking_const', {}),
            blue_walking_uncaught=data.get('blue_walking_uncaught', {}),
            blue_surfing_const=data.get('blue_surfing_const', {}),
            blue_surfing_uncaught=data.get('blue_surfing_uncaught', {}),
            blue_fishing_const=data.get('blue_fishing_const', {}),
            blue_fishing_uncaught=data.get('blue_fishing_uncaught', {}),
            blue_other_const=data.get('blue_other_const', {}),
            blue_other_uncaught=data.get('blue_other_uncaught', {}),
            yellow_all_const=data.get('yellow_all_const', []),
            yellow_all_uncaught=data.get('yellow_all_uncaught', []),
            yellow_walking_const=data.get('yellow_walking_const', {}),
            yellow_walking_uncaught=data.get('yellow_walking_uncaught', {}),
            yellow_surfing_const=data.get('yellow_surfing_const', {}),
            yellow_surfing_uncaught=data.get('yellow_surfing_uncaught', {}),
            yellow_fishing_const=data.get('yellow_fishing_const', {}),
            yellow_fishing_uncaught=data.get('yellow_fishing_uncaught', {}),
            yellow_other_const=data.get('yellow_other_const', {}),
            yellow_other_uncaught=data.get('yellow_other_uncaught', {}),
            caught=data.get('caught', []),
            evolvable=data.get('evolvable', []),
            devolvable=data.get('devolvable', [])
        )
    
    def update_pokemon_status_in_area(self, pokemon_name: str, modification_type: ModificationType = ModificationType.CATCH):
        """
        This method is only intended to handle marking a pokemon as caught in a specific area.
        If the game is tracking evolutions or devolutions this method will place eligible pokemon in the appropriate set, and remove them from other sets as appropriate.
        If the pokemon is not available in this area (i.e., not in any of the encounter lists for this area), this method will do nothing.
        If the pokemon is already marked as caught in this area, this method will do nothing.
        Arguments:
            pokemon_name: Name of the pokemon to mark as caught in this area.
            modification_type: Type of modification to make. Default is CATCH, but can be any appropriate type. For purposes of this method only CATCH, EVOLVE, and DEVOLVE are equivalent.

        Returns:
            None
        """
        pokemon_name = pokemon_name.lower()
        if pokemon_name in self.caught: #This check should always be false, but is here for safety
            return
        pokemon_available_in_area = False
        #Changed check to use the "const" lists, which are the full lists of pokemon available in this area, rather than the "uncaught" lists, which may be incomplete if the user has already caught some pokemon in this area
        #This ensures that if a user tries to mark a pokemon as caught in an area where it is not available, nothing will happen
        #This is important for ensuring that evolutions and devolutions are only tracked in areas where the pokemon is actually available
        #For example, if a user catches a Pikachu in Viridian Forest, then evolves it to Raichu, the Raichu should not be marked as caught in Viridian Forest
        #Similarly, if a user breeds a Pichu from a Pikachu, Pichu should not be marked as caught in Viridian Forest
        for encounter_type in [self.red_all_const, self.blue_all_const, self.yellow_all_const]:
            if not isinstance(encounter_type, list):
                continue
            if pokemon_name in encounter_type:
                pokemon_available_in_area = True
        if pokemon_available_in_area:
            #This check will be used for catching a pokemon, receiving a new pokemon via evolution, or gaining a new pokemon via breeding
            #In all these cases, the pokemon is considered "caught" in this area, and should be removed from uncaught lists
            if modification_type in [ModificationType.CATCH, ModificationType.EVOLVE, ModificationType.DEVOLVE]:
                self.caught.add(pokemon_name)
                if pokemon_name in self.evolvable:
                    self.evolvable.remove(pokemon_name)
                if pokemon_name in self.devolvable:
                    self.devolvable.remove(pokemon_name)
            #This check is used for marking a pokemon as eligible to get from evolution
            #In this case, the pokemon is not considered "caught" in this area, but is considered "evolvable"
            #So it is added to the evolvable set, and removed from the uncaught lists if tracked there. Needed for tracking evolutions properly
            #Note that pokemon will only appear if they are available to be caught in this area
            if modification_type == ModificationType.EVOLVABLE:
                self.evolvable.add(pokemon_name)
            #This check is used for marking a pokemon as eligible to get from devolution (e.g. breeding a baby pokemon)
            #In this case, the pokemon is not considered "caught" in this area, but is considered "devolvable"
            #So it is added to the devolvable set, and removed from the uncaught lists if tracked there. Needed for tracking devolutions properly
            #Note that pokemon will only appear if they are available to be caught in this area
            if modification_type == ModificationType.DEVOLVABLE:
                self.devolvable.add(pokemon_name)
            for encounter_type in [self.red_all_uncaught, self.blue_all_uncaught, self.yellow_all_uncaught]:
                if not isinstance(encounter_type, list):
                    continue
                if pokemon_name in encounter_type:
                    encounter_type.remove(pokemon_name)
            #Walking and Surfing encounters are stored as dicts of sublocations to lists of pokemon
            for encounter_type in [self.red_walking_uncaught, self.red_surfing_uncaught, self.blue_walking_uncaught, self.blue_surfing_uncaught, 
                                   self.yellow_walking_uncaught, self.yellow_surfing_uncaught]:
                if not isinstance(encounter_type, dict):
                    continue
                for sub_location in encounter_type:
                    if isinstance(encounter_type[sub_location], list) and pokemon_name in encounter_type[sub_location]:
                        encounter_type[sub_location].remove(pokemon_name)
            #Fishing and Other encounters are stored as dicts of sublocations to dicts of subtypes to lists of pokemon
            for encounter_type in [self.red_fishing_uncaught, self.red_other_uncaught, self.blue_fishing_uncaught, self.blue_other_uncaught,
                                   self.yellow_fishing_uncaught, self.yellow_other_uncaught]:
                if not isinstance(encounter_type, dict):
                    continue
                for sub_location in encounter_type:
                    if isinstance(encounter_type[sub_location], dict):
                        for subtype in encounter_type[sub_location]:
                            if isinstance(encounter_type[sub_location][subtype], list) and pokemon_name in encounter_type[sub_location][subtype]:
                                encounter_type[sub_location][subtype].remove(pokemon_name)
            

    def reset_pokemon_status_in_area(self, pokemon_name: str):
        """
        This method is a hard reset of all pokemon data in an area. It does not allow for modification of selected fields.
        It is intended to be used when a user wants to "uncatch" a pokemon in an area, for example if they made a mistake or want to re-catch a pokemon.
        It will remove the pokemon from the caught, evolvable, and devolvable sets, and add it back to all appropriate uncaught lists if it is available in this area.
        Arguments:
            pokemon_name: Name of the pokemon to reset in this area.
        Returns:
            None
        """
        pokemon_name = pokemon_name.lower()
        if pokemon_name in self.caught:
            self.caught.remove(pokemon_name)
        if pokemon_name in self.evolvable:
            self.evolvable.remove(pokemon_name)
        if pokemon_name in self.devolvable:
            self.devolvable.remove(pokemon_name)
        #Now we need to add the pokemon back to all appropriate uncaught lists if it is available in this area
        #We will use the "const" lists to determine if the pokemon is available in this area
        #If it is, we will add it back to the appropriate uncaught lists if it is not already present there
        #This ensures that if a user resets a pokemon that was never caught in this area, it will not be added to the uncaught lists
        
        #All encounter types are summarized here for simplicity, they should be lists of pokemon available in this area
        for encounter_type_uncaught, encounter_type_const in [(self.red_all_uncaught, self.red_all_const),
                                                              (self.blue_all_uncaught, self.blue_all_const),
                                                              (self.yellow_all_uncaught, self.yellow_all_const)]:
            if not isinstance(encounter_type_uncaught, list) or not isinstance(encounter_type_const, list):
                continue
            if pokemon_name in encounter_type_const and pokemon_name not in encounter_type_uncaught:
                encounter_type_uncaught.append(pokemon_name)
        #Walking and Surfing encounters are stored as dicts of sublocations to lists of pokemon
        for encounter_type_uncaught, encounter_type_const in [(self.red_walking_uncaught, self.red_walking_const),
                                                              (self.red_surfing_uncaught, self.red_surfing_const),
                                                              (self.blue_walking_uncaught, self.blue_walking_const),
                                                              (self.blue_surfing_uncaught, self.blue_surfing_const),
                                                              (self.yellow_walking_uncaught, self.yellow_walking_const),
                                                              (self.yellow_surfing_uncaught, self.yellow_surfing_const)]:
            if not isinstance(encounter_type_uncaught, dict) or not isinstance(encounter_type_const, dict):
                continue
            for sub_location in encounter_type_const:
                if isinstance(encounter_type_const[sub_location], list):
                    if sub_location not in encounter_type_uncaught or not isinstance(encounter_type_uncaught[sub_location], list):
                        encounter_type_uncaught[sub_location] = encounter_type_const[sub_location].copy()
                    if pokemon_name in encounter_type_const[sub_location] and pokemon_name not in encounter_type_uncaught[sub_location]:
                        encounter_type_uncaught[sub_location].append(pokemon_name)
        #Fishing and Other encounters are stored as dicts of sublocations to dicts of subtypes to lists of pokemon
        for encounter_type_uncaught, encounter_type_const in [(self.red_fishing_uncaught, self.red_fishing_const),
                                                              (self.red_other_uncaught, self.red_other_const),
                                                              (self.blue_fishing_uncaught, self.blue_fishing_const),
                                                              (self.blue_other_uncaught, self.blue_other_const),
                                                              (self.yellow_fishing_uncaught, self.yellow_fishing_const),
                                                              (self.yellow_other_uncaught, self.yellow_other_const)]:
            if not isinstance(encounter_type_uncaught, dict) or not isinstance(encounter_type_const, dict):
                continue
            for sub_location in encounter_type_const:
                if isinstance(encounter_type_const[sub_location], dict):
                    if sub_location not in encounter_type_uncaught or not isinstance(encounter_type_uncaught[sub_location], dict):
                        encounter_type_uncaught[sub_location] = {subtype: encounter_type_const[sub_location][subtype].copy() for subtype in encounter_type_const[sub_location]}
                    for subtype in encounter_type_const[sub_location]:
                        if subtype not in encounter_type_uncaught[sub_location] or not isinstance(encounter_type_uncaught[sub_location][subtype], list):
                            encounter_type_uncaught[sub_location][subtype] = encounter_type_const[sub_location][subtype].copy()
                        if pokemon_name in encounter_type_const[sub_location][subtype] and pokemon_name not in encounter_type_uncaught[sub_location][subtype]:
                            encounter_type_uncaught[sub_location][subtype].append(pokemon_name)
                elif isinstance(encounter_type_const[sub_location], list): #should never happen, but is here for safety
                    if sub_location not in encounter_type_uncaught or not isinstance(encounter_type_uncaught[sub_location], list):
                        encounter_type_uncaught[sub_location] = encounter_type_const[sub_location].copy()
                    if pokemon_name in encounter_type_const[sub_location] and pokemon_name not in encounter_type_uncaught[sub_location]:
                        encounter_type_uncaught[sub_location].append(pokemon_name)

    def uncaught_fields(self):
        """
        Returns a dictionary of uncaught pokemon lists for each game and encounter type.
        Needed here since it will be unique to each generation.
        The structure is:
        SupporedGame -> Encounter Type Field
        """
        return {
            SupportedGames.RED: {
                'All': self.red_all_uncaught,
                'Walking': self.red_walking_uncaught,
                'Surfing': self.red_surfing_uncaught,
                'Fishing': self.red_fishing_uncaught,
                'Other': self.red_other_uncaught
            },
            SupportedGames.BLUE: {
                'All': self.blue_all_uncaught,
                'Walking': self.blue_walking_uncaught,
                'Surfing': self.blue_surfing_uncaught,
                'Fishing': self.blue_fishing_uncaught,
                'Other': self.blue_other_uncaught
            },
            SupportedGames.YELLOW: {
                'All': self.yellow_all_uncaught,
                'Walking': self.yellow_walking_uncaught,
                'Surfing': self.yellow_surfing_uncaught,
                'Fishing': self.yellow_fishing_uncaught,
                'Other': self.yellow_other_uncaught
            }
        }
    
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'red_all_const': self.red_all_const,
            'red_all_uncaught': self.red_all_uncaught,
            'red_walking_const': self.red_walking_const,
            'red_walking_uncaught': self.red_walking_uncaught,
            'red_surfing_const': self.red_surfing_const,
            'red_surfing_uncaught': self.red_surfing_uncaught,
            'red_fishing_const': self.red_fishing_const,
            'red_fishing_uncaught': self.red_fishing_uncaught,
            'red_other_const': self.red_other_const,
            'red_other_uncaught': self.red_other_uncaught,
            'blue_all_const': self.blue_all_const,
            'blue_all_uncaught': self.blue_all_uncaught,
            'blue_walking_const': self.blue_walking_const,
            'blue_walking_uncaught': self.blue_walking_uncaught,
            'blue_surfing_const': self.blue_surfing_const,
            'blue_surfing_uncaught': self.blue_surfing_uncaught,
            'blue_fishing_const': self.blue_fishing_const,
            'blue_fishing_uncaught': self.blue_fishing_uncaught,
            'blue_other_const': self.blue_other_const,
            'blue_other_uncaught': self.blue_other_uncaught,
            'yellow_all_const': self.yellow_all_const,
            'yellow_all_uncaught': self.yellow_all_uncaught,
            'yellow_walking_const': self.yellow_walking_const,
            'yellow_walking_uncaught': self.yellow_walking_uncaught,
            'yellow_surfing_const': self.yellow_surfing_const,
            'yellow_surfing_uncaught': self.yellow_surfing_uncaught,
            'yellow_fishing_const': self.yellow_fishing_const,
            'yellow_fishing_uncaught': self.yellow_fishing_uncaught,
            'yellow_other_const': self.yellow_other_const,
            'yellow_other_uncaught': self.yellow_other_uncaught
        })
        return base_dict


    def __repr__(self):
        lines = [f"Gen1 Location Name: {self.name}"]
        
        if self.red_walking_const:
            lines.append(f"Red Walking: {self.red_walking_const}")
        if self.red_surfing_const:
            lines.append(f"Red Surfing: {self.red_surfing_const}")
        if self.red_fishing_const:
            lines.append(f"Red Fishing: {self.red_fishing_const}")
        if self.red_other_const:
            lines.append(f"Red Other: {self.red_other_const}")
        if self.blue_walking_const:
            lines.append(f"Blue Walking: {self.blue_walking_const}")
        if self.blue_surfing_const:
            lines.append(f"Blue Surfing: {self.blue_surfing_const}")
        if self.blue_fishing_const:
            lines.append(f"Blue Fishing: {self.blue_fishing_const}")
        if self.blue_other_const:
            lines.append(f"Blue Other: {self.blue_other_const}")
        if self.yellow_walking_const:
            lines.append(f"Yellow Walking: {self.yellow_walking_const}")
        if self.yellow_surfing_const:
            lines.append(f"Yellow Surfing: {self.yellow_surfing_const}")
        if self.yellow_fishing_const:
            lines.append(f"Yellow Fishing: {self.yellow_fishing_const}")
        if self.yellow_other_const:
            lines.append(f"Yellow Other: {self.yellow_other_const}")
        
        return ",\n".join(lines)