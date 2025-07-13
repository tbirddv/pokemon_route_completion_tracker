import copy
from Data.constants import SupportedGames

class Location:
    def __init__(self, name, caught = None):
        self.name = name
        self.caught = set(caught) if caught is not None else set()

    def to_dict(self):
        return {
            'name': self.name,
            'caught': list(self.caught)
        }

class Gen1Location(Location):
    def __init__(self, name, red_walking_const, red_walking_uncaught,
                 red_surfing_const, red_surfing_uncaught,
                 red_fishing_const, red_fishing_uncaught,
                 red_other_const, red_other_uncaught,
                 blue_walking_const, blue_walking_uncaught,
                 blue_surfing_const, blue_surfing_uncaught,
                 blue_fishing_const, blue_fishing_uncaught,
                 blue_other_const, blue_other_uncaught,
                 yellow_walking_const, yellow_walking_uncaught,
                 yellow_surfing_const, yellow_surfing_uncaught,
                 yellow_fishing_const, yellow_fishing_uncaught,
                 yellow_other_const, yellow_other_uncaught, caught = None):
        super().__init__(name, caught)
        self.red_walking_const = red_walking_const
        self.red_walking_uncaught = red_walking_uncaught
        self.red_surfing_const = red_surfing_const
        self.red_surfing_uncaught = red_surfing_uncaught
        self.red_fishing_const = red_fishing_const
        self.red_fishing_uncaught = red_fishing_uncaught
        self.red_other_const = red_other_const
        self.red_other_uncaught = red_other_uncaught
        self.blue_walking_const = blue_walking_const
        self.blue_walking_uncaught = blue_walking_uncaught
        self.blue_surfing_const = blue_surfing_const
        self.blue_surfing_uncaught = blue_surfing_uncaught
        self.blue_fishing_const = blue_fishing_const
        self.blue_fishing_uncaught = blue_fishing_uncaught
        self.blue_other_const = blue_other_const
        self.blue_other_uncaught = blue_other_uncaught
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
        red_walking_const = {subloc.strip(): [mon.strip() for mon in pokemon.strip().split('/') if mon.strip() != '' and mon.strip().lower() != "none"]
                             for subloc, pokemon in (sublocation.strip().split(':') for sublocation in row['Red Walking'].strip().split(';') if sublocation.strip() != '' and sublocation.strip().lower() != "none" and len(sublocation.split(':')) == 2)
                               if subloc.strip() != '' and subloc.strip().lower() != "none" and pokemon.strip() != '' and pokemon.strip().lower() != "none"}
        red_walking_uncaught = copy.deepcopy(red_walking_const)
        red_surfing_const = {subloc.strip(): [mon.strip() for mon in pokemon.strip().split('/') if mon.strip() != '' and mon.strip().lower() != "none"]
                             for subloc, pokemon in (sublocation.strip().split(':') for sublocation in row['Red Surfing'].strip().split(';') if sublocation.strip() != '' and sublocation.strip().lower() != "none" and len(sublocation.split(':')) == 2)
                               if subloc.strip() != '' and subloc.strip().lower() != "none" and pokemon.strip() != '' and pokemon.strip().lower() != "none"}
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
                            red_fishing_const[subloc_name] = {subtype.split(':')[0].strip(): [pokemon.strip() for pokemon in subtype.split(':')[1].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
                                                             for subtype in subtypes if ':' in subtype and len(subtype.split(':')) == 2 and subtype.split(':')[1].strip() != '' and subtype.split(':')[1].strip().lower() != "none"}
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
                            red_other_const[subloc_name] = {subtype.split(':')[0].strip(): [pokemon.strip() for pokemon in subtype.split(':')[1].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
                                                             for subtype in subtypes if ':' in subtype and len(subtype.split(':')) == 2 and subtype.split(':')[1].strip() != '' and subtype.split(':')[1].strip().lower() != "none"}
        red_other_uncaught = copy.deepcopy(red_other_const)
        blue_walking_const = {subloc.strip(): [mon.strip() for mon in pokemon.strip().split('/') if mon.strip() != '' and mon.strip().lower() != "none"]
                             for subloc, pokemon in (sublocation.strip().split(':') for sublocation in row['Blue Walking'].strip().split(';') if sublocation.strip() != '' and sublocation.strip().lower() != "none" and len(sublocation.split(':')) == 2)
                               if subloc.strip() != '' and subloc.strip().lower() != "none" and pokemon.strip() != '' and pokemon.strip().lower() != "none"}
        blue_walking_uncaught = copy.deepcopy(blue_walking_const)
        blue_surfing_const = {subloc.strip(): [mon.strip() for mon in pokemon.strip().split('/') if mon.strip() != '' and mon.strip().lower() != "none"]
                             for subloc, pokemon in (sublocation.strip().split(':') for sublocation in row['Blue Surfing'].strip().split(';') if sublocation.strip() != '' and sublocation.strip().lower() != "none" and len(sublocation.split(':')) == 2)
                               if subloc.strip() != '' and subloc.strip().lower() != "none" and pokemon.strip() != '' and pokemon.strip().lower() != "none"}
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
                            blue_fishing_const[subloc_name] = {subtype.split(':')[0].strip(): [pokemon.strip() for pokemon in subtype.split(':')[1].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
                                                             for subtype in subtypes if ':' in subtype and len(subtype.split(':')) == 2 and subtype.split(':')[1].strip() != '' and subtype.split(':')[1].strip().lower() != "none"}
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
                            blue_other_const[subloc_name] = {subtype.split(':')[0].strip(): [pokemon.strip() for pokemon in subtype.split(':')[1].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
                                                             for subtype in subtypes if ':' in subtype and len(subtype.split(':')) == 2 and subtype.split(':')[1].strip() != '' and subtype.split(':')[1].strip().lower() != "none"}
        blue_other_uncaught = copy.deepcopy(blue_other_const)
        yellow_walking_const = {subloc.strip(): [mon.strip() for mon in pokemon.strip().split('/') if mon.strip() != '' and mon.strip().lower() != "none"]
                             for subloc, pokemon in (sublocation.strip().split(':') for sublocation in row['Yellow Walking'].strip().split(';') if sublocation.strip() != '' and sublocation.strip().lower() != "none" and len(sublocation.split(':')) == 2)
                               if subloc.strip() != '' and subloc.strip().lower() != "none" and pokemon.strip() != '' and pokemon.strip().lower() != "none"}
        yellow_walking_uncaught = copy.deepcopy(yellow_walking_const)
        yellow_surfing_const = {subloc.strip(): [mon.strip() for mon in pokemon.strip().split('/') if mon.strip() != '' and mon.strip().lower() != "none"]
                             for subloc, pokemon in (sublocation.strip().split(':') for sublocation in row['Yellow Surfing'].strip().split(';') if sublocation.strip() != '' and sublocation.strip().lower() != "none" and len(sublocation.split(':')) == 2)
                               if subloc.strip() != '' and subloc.strip().lower() != "none" and pokemon.strip() != '' and pokemon.strip().lower() != "none"}
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
                            yellow_fishing_const[subloc_name] = {subtype.split(':')[0].strip(): [pokemon.strip() for pokemon in subtype.split(':')[1].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
                                                             for subtype in subtypes if ':' in subtype and len(subtype.split(':')) == 2 and subtype.split(':')[1].strip() != '' and subtype.split(':')[1].strip().lower() != "none"}
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
                            yellow_other_const[subloc_name] = {subtype.split(':')[0].strip(): [pokemon.strip() for pokemon in subtype.split(':')[1].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
                                                             for subtype in subtypes if ':' in subtype and len(subtype.split(':')) == 2 and subtype.split(':')[1].strip() != '' and subtype.split(':')[1].strip().lower() != "none"}
        yellow_other_uncaught = copy.deepcopy(yellow_other_const)
        return cls(name, red_walking_const, red_walking_uncaught,
                   red_surfing_const, red_surfing_uncaught,
                   red_fishing_const, red_fishing_uncaught,
                   red_other_const, red_other_uncaught,
                   blue_walking_const, blue_walking_uncaught,
                   blue_surfing_const, blue_surfing_uncaught,
                   blue_fishing_const, blue_fishing_uncaught,
                   blue_other_const, blue_other_uncaught,
                   yellow_walking_const, yellow_walking_uncaught,
                   yellow_surfing_const, yellow_surfing_uncaught,
                   yellow_fishing_const, yellow_fishing_uncaught,
                   yellow_other_const, yellow_other_uncaught)
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            red_walking_const=data.get('red_walking_const', {}),
            red_walking_uncaught=data.get('red_walking_uncaught', {}),
            red_surfing_const=data.get('red_surfing_const', {}),
            red_surfing_uncaught=data.get('red_surfing_uncaught', {}),
            red_fishing_const=data.get('red_fishing_const', {}),
            red_fishing_uncaught=data.get('red_fishing_uncaught', {}),
            red_other_const=data.get('red_other_const', {}),
            red_other_uncaught=data.get('red_other_uncaught', {}),
            blue_walking_const=data.get('blue_walking_const', {}),
            blue_walking_uncaught=data.get('blue_walking_uncaught', {}),
            blue_surfing_const=data.get('blue_surfing_const', {}),
            blue_surfing_uncaught=data.get('blue_surfing_uncaught', {}),
            blue_fishing_const=data.get('blue_fishing_const', {}),
            blue_fishing_uncaught=data.get('blue_fishing_uncaught', {}),
            blue_other_const=data.get('blue_other_const', {}),
            blue_other_uncaught=data.get('blue_other_uncaught', {}),
            yellow_walking_const=data.get('yellow_walking_const', {}),
            yellow_walking_uncaught=data.get('yellow_walking_uncaught', {}),
            yellow_surfing_const=data.get('yellow_surfing_const', {}),
            yellow_surfing_uncaught=data.get('yellow_surfing_uncaught', {}),
            yellow_fishing_const=data.get('yellow_fishing_const', {}),
            yellow_fishing_uncaught=data.get('yellow_fishing_uncaught', {}),
            yellow_other_const=data.get('yellow_other_const', {}),
            yellow_other_uncaught=data.get('yellow_other_uncaught', {}),
            caught=data.get('caught', [])
        )
    
    def mark_pokemon_caught_in_area(self, pokemon_name: str):
        pokemon_available_in_area = False
        for encounter_type in [self.red_walking_uncaught, self.red_surfing_uncaught, self.red_fishing_uncaught, self.red_other_uncaught,
                         self.blue_walking_uncaught, self.blue_surfing_uncaught, self.blue_fishing_uncaught, self.blue_other_uncaught,
                         self.yellow_walking_uncaught, self.yellow_surfing_uncaught, self.yellow_fishing_uncaught, self.yellow_other_uncaught]:
            if not isinstance(encounter_type, dict):
                continue
            for sub_location in encounter_type:
                if isinstance(encounter_type[sub_location], list):
                    if pokemon_name in encounter_type[sub_location]:
                        pokemon_available_in_area = True
                        encounter_type[sub_location].remove(pokemon_name)
                elif isinstance(encounter_type[sub_location], dict):
                    for subtype in encounter_type[sub_location]:
                        if pokemon_name in encounter_type[sub_location][subtype]:
                            encounter_type[sub_location][subtype].remove(pokemon_name)
                            pokemon_available_in_area = True
        if pokemon_available_in_area:
            self.caught.add(pokemon_name)

    def reset_pokemon_status_in_area(self, pokemon_name: str):
        if pokemon_name in self.caught:
            self.caught.remove(pokemon_name)
        for encounter_type_uncaught, encounter_type_const in [(self.red_walking_uncaught, self.red_walking_const),
                                                              (self.red_surfing_uncaught, self.red_surfing_const),
                                                              (self.red_fishing_uncaught, self.red_fishing_const),
                                                              (self.red_other_uncaught, self.red_other_const),
                                                              (self.blue_walking_uncaught, self.blue_walking_const),
                                                              (self.blue_surfing_uncaught, self.blue_surfing_const),
                                                              (self.blue_fishing_uncaught, self.blue_fishing_const),
                                                              (self.blue_other_uncaught, self.blue_other_const),
                                                              (self.yellow_walking_uncaught, self.yellow_walking_const),
                                                              (self.yellow_surfing_uncaught, self.yellow_surfing_const),
                                                              (self.yellow_fishing_uncaught, self.yellow_fishing_const),
                                                              (self.yellow_other_uncaught, self.yellow_other_const)]:
            if not isinstance(encounter_type_uncaught, dict) or not isinstance(encounter_type_const, dict):
                continue
            for sub_location in encounter_type_const:
                if isinstance(encounter_type_const[sub_location], list):
                    if sub_location not in encounter_type_uncaught or not isinstance(encounter_type_uncaught[sub_location], list):
                        encounter_type_uncaught[sub_location] = encounter_type_const[sub_location].copy()
                    if pokemon_name in encounter_type_const[sub_location] and pokemon_name not in encounter_type_uncaught[sub_location]:
                        encounter_type_uncaught[sub_location].append(pokemon_name)
                elif isinstance(encounter_type_const[sub_location], dict):
                    if sub_location not in encounter_type_uncaught or not isinstance(encounter_type_uncaught[sub_location], dict):
                        encounter_type_uncaught[sub_location] = {subtype: encounter_type_const[sub_location][subtype].copy() for subtype in encounter_type_const[sub_location]}
                    for subtype in encounter_type_const[sub_location]:
                        if subtype not in encounter_type_uncaught[sub_location]:
                            encounter_type_uncaught[sub_location][subtype] = encounter_type_const[sub_location][subtype].copy()
                        if pokemon_name in encounter_type_const[sub_location][subtype] and pokemon_name not in encounter_type_uncaught[sub_location][subtype]:
                            encounter_type_uncaught[sub_location][subtype].append(pokemon_name)

    def uncaught_fields(self):
        return {
            SupportedGames.RED: {
                'Walking': self.red_walking_uncaught,
                'Surfing': self.red_surfing_uncaught,
                'Fishing': self.red_fishing_uncaught,
                'Other': self.red_other_uncaught
            },
            SupportedGames.BLUE: {
                'Walking': self.blue_walking_uncaught,
                'Surfing': self.blue_surfing_uncaught,
                'Fishing': self.blue_fishing_uncaught,
                'Other': self.blue_other_uncaught
            },
            SupportedGames.YELLOW: {
                'Walking': self.yellow_walking_uncaught,
                'Surfing': self.yellow_surfing_uncaught,
                'Fishing': self.yellow_fishing_uncaught,
                'Other': self.yellow_other_uncaught
            }
        }
        

    
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'red_walking_const': self.red_walking_const,
            'red_walking_uncaught': self.red_walking_uncaught,
            'red_surfing_const': self.red_surfing_const,
            'red_surfing_uncaught': self.red_surfing_uncaught,
            'red_fishing_const': self.red_fishing_const,
            'red_fishing_uncaught': self.red_fishing_uncaught,
            'red_other_const': self.red_other_const,
            'red_other_uncaught': self.red_other_uncaught,
            'blue_walking_const': self.blue_walking_const,
            'blue_walking_uncaught': self.blue_walking_uncaught,
            'blue_surfing_const': self.blue_surfing_const,
            'blue_surfing_uncaught': self.blue_surfing_uncaught,
            'blue_fishing_const': self.blue_fishing_const,
            'blue_fishing_uncaught': self.blue_fishing_uncaught,
            'blue_other_const': self.blue_other_const,
            'blue_other_uncaught': self.blue_other_uncaught,
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