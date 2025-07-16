import copy
from enum import Enum
from Data.constants import SupportedGames, generation_1_encounter_column_name_mappings

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

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            caught=data.get('caught', []),
            evolvable=data.get('evolvable', []),
            devolvable=data.get('devolvable', [])
        )

    def to_dict(self):
        return {
            'name': self.name,
            'caught': list(self.caught),
            'evolvable': list(self.evolvable),
            'devolvable': list(self.devolvable)
        }

class Gen1Location(Location):
    def __init__(self, name, encounter_data, caught = None, evolvable = None, devolvable = None):
        super().__init__(name, caught, evolvable, devolvable)
        self.encounter_data = encounter_data

    @staticmethod
    def _process_walking_or_surfing(encounter_string):
        return {subloc.strip(): [mon.strip().lower() for mon in pokemon.strip().split('/') if mon.strip() != '' and mon.strip().lower() != "none"]
                for subloc, pokemon in (sublocation.strip().split(':') for sublocation in encounter_string.strip().split(';') if sublocation.strip() != '' and sublocation.strip().lower() != "none" and len(sublocation.split(':')) == 2)
                if subloc.strip() != '' and subloc.strip().lower() != "none" and pokemon.strip() != '' and pokemon.strip().lower() != "none"}
    
    @staticmethod
    def _process_fishing_or_other(encounter_string):
        encounter_dict = {}
        if encounter_string.strip() != '' and encounter_string.strip().lower() != "none":
            fishing_sublocations = encounter_string.strip().split(';')
            for sublocation in fishing_sublocations:
                sublocation = sublocation.strip()
                if sublocation.lower() != "none" and sublocation != '':
                    parts = sublocation.split('~')
                    if parts and len(parts) > 1:
                        subloc_name = parts[0].strip()
                        if subloc_name.lower() != "none" and subloc_name != '':
                            subtypes = [part.strip() for part in parts[1:] if part.strip() != '' and part.strip().lower() != "none"]
                            encounter_dict[subloc_name] = {subtype.split(':')[0].strip(): [pokemon.strip().lower() for pokemon in subtype.split(':')[1].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
                                                           for subtype in subtypes if ':' in subtype and len(subtype.split(':')) == 2 and subtype.split(':')[1].strip() != '' and subtype.split(':')[1].strip().lower() != "none"}
        return encounter_dict
    
    @staticmethod
    def _process_area_summary(walking_dict, surfing_dict, fishing_dict, other_dict):
        summary = set()
        for encounter_dict in [walking_dict, surfing_dict, fishing_dict, other_dict]:
            if isinstance(encounter_dict, dict):
                for sub_item in encounter_dict.values():
                    if isinstance(sub_item, list):
                        summary.update(sub_item)
                    elif isinstance(sub_item, dict):
                        for pokemon_list in sub_item.values():
                            if isinstance(pokemon_list, list):
                                summary.update(pokemon_list)
        return list(summary)

    @classmethod
    def from_csv(cls, row):
        name = row['Area Name']
        encounter_data = {}
        for game, columns in generation_1_encounter_column_name_mappings.items():
            walking_dict = cls._process_walking_or_surfing(row[columns['walking']])
            surfing_dict = cls._process_walking_or_surfing(row[columns['surfing']])
            fishing_dict = cls._process_fishing_or_other(row[columns['fishing']])
            other_dict = cls._process_fishing_or_other(row[columns['other']])
            all_summary = cls._process_area_summary(walking_dict, surfing_dict, fishing_dict, other_dict)

            encounter_data[game.value] = {
                'const': {
                    'All': all_summary,
                    'Walking': walking_dict,
                    'Surfing': surfing_dict,
                    'Fishing': fishing_dict,
                    'Other': other_dict
                },
                'uncaught': {
                    'All': copy.deepcopy(all_summary),
                    'Walking': copy.deepcopy(walking_dict),
                    'Surfing': copy.deepcopy(surfing_dict),
                    'Fishing': copy.deepcopy(fishing_dict),
                    'Other': copy.deepcopy(other_dict)
                }
            }
        return cls(name, encounter_data)
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            encounter_data=data.get('encounter_data', {}),
            caught=data.get('caught', []),
            evolvable=data.get('evolvable', []),
            devolvable=data.get('devolvable', [])
        )
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict['encounter_data'] = self.encounter_data
        return base_dict
    
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
        for game_data in self.encounter_data.values():
            if not isinstance(game_data['const']['All'], list):
                continue
            if pokemon_name in game_data['const']['All']:
                pokemon_available_in_area = True
                break
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
            for game_data in self.encounter_data.values():
                if not isinstance(game_data['uncaught']['All'], list):
                    continue
                if pokemon_name in game_data['uncaught']['All']:
                    game_data['uncaught']['All'].remove(pokemon_name)
                #Walking and Surfing encounters are stored as dicts of sublocations to lists of pokemon
                for encounter_type in [game_data['uncaught']['Walking'], game_data['uncaught']['Surfing']]:
                    if not isinstance(encounter_type, dict):
                        continue
                    for sub_location in encounter_type:
                        if isinstance(encounter_type[sub_location], list) and pokemon_name in encounter_type[sub_location]:
                            encounter_type[sub_location].remove(pokemon_name)
                #Fishing and Other encounters are stored as dicts of sublocations to dicts of subtypes to lists of pokemon
                for encounter_type in [game_data['uncaught']['Fishing'], game_data['uncaught']['Other']]:
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
        for game_data in self.encounter_data.values():
            if not isinstance(game_data['uncaught']['All'], list) or not isinstance(game_data['const']['All'], list):
                continue
            if pokemon_name in game_data['const']['All'] and pokemon_name not in game_data['uncaught']['All']:
                game_data['uncaught']['All'].append(pokemon_name)
        #Walking and Surfing encounters are stored as dicts of sublocations to lists of pokemon
            for encounter_type_uncaught, encounter_type_const in [(game_data['uncaught']['Walking'], game_data['const']['Walking']),
                                                              (game_data['uncaught']['Surfing'], game_data['const']['Surfing']),]:
                if not isinstance(encounter_type_uncaught, dict) or not isinstance(encounter_type_const, dict):
                    continue
                for sub_location in encounter_type_const:
                    if isinstance(encounter_type_const[sub_location], list):
                        if sub_location not in encounter_type_uncaught or not isinstance(encounter_type_uncaught[sub_location], list):
                            encounter_type_uncaught[sub_location] = encounter_type_const[sub_location].copy()
                        if pokemon_name in encounter_type_const[sub_location] and pokemon_name not in encounter_type_uncaught[sub_location]:
                            encounter_type_uncaught[sub_location].append(pokemon_name)
        #Fishing and Other encounters are stored as dicts of sublocations to dicts of subtypes to lists of pokemon
            for encounter_type_uncaught, encounter_type_const in [[game_data['uncaught']['Fishing'], game_data['const']['Fishing']],
                                                                  [game_data['uncaught']['Other'], game_data['const']['Other']]]:
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
