import copy

class Location:
    def __init__(self, name):
        self.name = name
        self.caught = []

class Gen1Location(Location):
    def __init__(self, name, red_walking, red_surfing, red_fishing, red_other,
                 blue_walking, blue_surfing, blue_fishing, blue_other,
                 yellow_walking, yellow_surfing, yellow_fishing, yellow_other):
        super().__init__(name)
        self.red_walking_const = {subloc.strip(): [mon.strip() for mon in pokemon.strip().split('/') if mon.strip() != '' and mon.strip().lower() != "none"]
                             for subloc, pokemon in (sublocation.strip().split(':') for sublocation in red_walking.strip().split(';') if sublocation.strip() != '' and sublocation.strip().lower() != "none" and len(sublocation.split(':')) == 2)
                               if subloc.strip() != '' and subloc.strip().lower() != "none" and pokemon.strip() != '' and pokemon.strip().lower() != "none"}
        self.red_walking_uncaught = copy.deepcopy(self.red_walking_const)
        self.red_surfing_const = {subloc.strip(): [mon.strip() for mon in pokemon.strip().split('/') if mon.strip() != '' and mon.strip().lower() != "none"]
                             for subloc, pokemon in (sublocation.strip().split(':') for sublocation in red_surfing.strip().split(';') if sublocation.strip() != '' and sublocation.strip().lower() != "none" and len(sublocation.split(':')) == 2)
                               if subloc.strip() != '' and subloc.strip().lower() != "none" and pokemon.strip() != '' and pokemon.strip().lower() != "none"}
        self.red_surfing_uncaught = copy.deepcopy(self.red_surfing_const)
        self.red_fishing_const = {}
        if red_fishing.strip() != '' and red_fishing.strip().lower() != "none":
            fishing_sublocations = red_fishing.strip().split(';')
            for sublocation in fishing_sublocations:
                sublocation = sublocation.strip()
                if sublocation.lower() != "none" and sublocation != '':
                    parts = sublocation.split('~')
                    if parts and len(parts) > 1:
                        subloc_name = parts[0].strip()
                        if subloc_name.lower() != "none" and subloc_name != '':
                            subtypes = [part.strip() for part in parts[1:] if part.strip() != '' and part.strip().lower() != "none"]
                            self.red_fishing_const[subloc_name] = {subtype.split(':')[0].strip(): [pokemon.strip() for pokemon in subtype.split(':')[1].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
                                                             for subtype in subtypes if ':' in subtype and len(subtype.split(':')) == 2 and subtype.split(':')[1].strip() != '' and subtype.split(':')[1].strip().lower() != "none"}
        self.red_fishing_uncaught = copy.deepcopy(self.red_fishing_const)
        self.red_other_const = {}
        if red_other.strip() != '' and red_other.strip().lower() != "none":
            other_sublocations = red_other.strip().split(';')
            for sublocation in other_sublocations:
                sublocation = sublocation.strip()
                if sublocation.lower() != "none" and sublocation != '':
                    parts = sublocation.split('~')
                    if parts and len(parts) > 1:
                        subloc_name = parts[0].strip()
                        if subloc_name.lower() != "none" and subloc_name != '':
                            subtypes = [part.strip() for part in parts[1:] if part.strip() != '' and part.strip().lower() != "none"]
                            self.red_other_const[subloc_name] = {subtype.split(':')[0].strip(): [pokemon.strip() for pokemon in subtype.split(':')[1].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
                                                             for subtype in subtypes if ':' in subtype and len(subtype.split(':')) == 2 and subtype.split(':')[1].strip() != '' and subtype.split(':')[1].strip().lower() != "none"}
        self.red_other_uncaught = copy.deepcopy(self.red_other_const)
        self.blue_walking_const = {subloc.strip(): [mon.strip() for mon in pokemon.strip().split('/') if mon.strip() != '' and mon.strip().lower() != "none"]
                             for subloc, pokemon in (sublocation.strip().split(':') for sublocation in blue_walking.strip().split(';') if sublocation.strip() != '' and sublocation.strip().lower() != "none" and len(sublocation.split(':')) == 2)
                               if subloc.strip() != '' and subloc.strip().lower() != "none" and pokemon.strip() != '' and pokemon.strip().lower() != "none"}
        self.blue_walking_uncaught = copy.deepcopy(self.blue_walking_const)
        self.blue_surfing_const = {subloc.strip(): [mon.strip() for mon in pokemon.strip().split('/') if mon.strip() != '' and mon.strip().lower() != "none"]
                             for subloc, pokemon in (sublocation.strip().split(':') for sublocation in blue_surfing.strip().split(';') if sublocation.strip() != '' and sublocation.strip().lower() != "none" and len(sublocation.split(':')) == 2)
                               if subloc.strip() != '' and subloc.strip().lower() != "none" and pokemon.strip() != '' and pokemon.strip().lower() != "none"}
        self.blue_surfing_uncaught = copy.deepcopy(self.blue_surfing_const)
        self.blue_fishing_const = {}
        if blue_fishing.strip() != '' and blue_fishing.strip().lower() != "none":
            fishing_sublocations = blue_fishing.strip().split(';')
            for sublocation in fishing_sublocations:
                sublocation = sublocation.strip()
                if sublocation.lower() != "none" and sublocation != '':
                    parts = sublocation.split('~')
                    if parts and len(parts) > 1:
                        subloc_name = parts[0].strip()
                        if subloc_name.lower() != "none" and subloc_name != '':
                            subtypes = [part.strip() for part in parts[1:] if part.strip() != '' and part.strip().lower() != "none"]
                            self.blue_fishing_const[subloc_name] = {subtype.split(':')[0].strip(): [pokemon.strip() for pokemon in subtype.split(':')[1].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
                                                             for subtype in subtypes if ':' in subtype and len(subtype.split(':')) == 2 and subtype.split(':')[1].strip() != '' and subtype.split(':')[1].strip().lower() != "none"}
        self.blue_fishing_uncaught = copy.deepcopy(self.blue_fishing_const)
        self.blue_other_const = {}
        if blue_other.strip() != '' and blue_other.strip().lower() != "none":
            other_sublocations = blue_other.strip().split(';')
            for sublocation in other_sublocations:
                sublocation = sublocation.strip()
                if sublocation.lower() != "none" and sublocation != '':
                    parts = sublocation.split('~')
                    if parts and len(parts) > 1:
                        subloc_name = parts[0].strip()
                        if subloc_name.lower() != "none" and subloc_name != '':
                            subtypes = [part.strip() for part in parts[1:] if part.strip() != '' and part.strip().lower() != "none"]
                            self.blue_other_const[subloc_name] = {subtype.split(':')[0].strip(): [pokemon.strip() for pokemon in subtype.split(':')[1].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
                                                             for subtype in subtypes if ':' in subtype and len(subtype.split(':')) == 2 and subtype.split(':')[1].strip() != '' and subtype.split(':')[1].strip().lower() != "none"}
        self.blue_other_uncaught = copy.deepcopy(self.blue_other_const)
        self.yellow_walking_const = {subloc.strip(): [mon.strip() for mon in pokemon.strip().split('/') if mon.strip() != '' and mon.strip().lower() != "none"]
                             for subloc, pokemon in (sublocation.strip().split(':') for sublocation in yellow_walking.strip().split(';') if sublocation.strip() != '' and sublocation.strip().lower() != "none" and len(sublocation.split(':')) == 2)
                               if subloc.strip() != '' and subloc.strip().lower() != "none" and pokemon.strip() != '' and pokemon.strip().lower() != "none"}
        self.yellow_walking_uncaught = copy.deepcopy(self.yellow_walking_const)
        self.yellow_surfing_const = {subloc.strip(): [mon.strip() for mon in pokemon.strip().split('/') if mon.strip() != '' and mon.strip().lower() != "none"]
                             for subloc, pokemon in (sublocation.strip().split(':') for sublocation in yellow_surfing.strip().split(';') if sublocation.strip() != '' and sublocation.strip().lower() != "none" and len(sublocation.split(':')) == 2)
                               if subloc.strip() != '' and subloc.strip().lower() != "none" and pokemon.strip() != '' and pokemon.strip().lower() != "none"}
        self.yellow_surfing_uncaught = copy.deepcopy(self.yellow_surfing_const)
        self.yellow_fishing_const = {}
        if yellow_fishing.strip() != '' and yellow_fishing.strip().lower() != "none":
            fishing_sublocations = yellow_fishing.strip().split(';')
            for sublocation in fishing_sublocations:
                sublocation = sublocation.strip()
                if sublocation.lower() != "none" and sublocation != '':
                    parts = sublocation.split('~')
                    if parts and len(parts) > 1:
                        subloc_name = parts[0].strip()
                        if subloc_name.lower() != "none" and subloc_name != '':
                            subtypes = [part.strip() for part in parts[1:] if part.strip() != '' and part.strip().lower() != "none"]
                            self.yellow_fishing_const[subloc_name] = {subtype.split(':')[0].strip(): [pokemon.strip() for pokemon in subtype.split(':')[1].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
                                                             for subtype in subtypes if ':' in subtype and len(subtype.split(':')) == 2 and subtype.split(':')[1].strip() != '' and subtype.split(':')[1].strip().lower() != "none"}
        self.yellow_fishing_uncaught = copy.deepcopy(self.yellow_fishing_const)
        self.yellow_other_const = {}
        if yellow_other.strip() != '' and yellow_other.strip().lower() != "none":
            other_sublocations = yellow_other.strip().split(';')
            for sublocation in other_sublocations:
                sublocation = sublocation.strip()
                if sublocation.lower() != "none" and sublocation != '':
                    parts = sublocation.split('~')
                    if parts and len(parts) > 1:
                        subloc_name = parts[0].strip()
                        if subloc_name.lower() != "none" and subloc_name != '':
                            subtypes = [part.strip() for part in parts[1:] if part.strip() != '' and part.strip().lower() != "none"]
                            self.yellow_other_const[subloc_name] = {subtype.split(':')[0].strip(): [pokemon.strip() for pokemon in subtype.split(':')[1].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
                                                             for subtype in subtypes if ':' in subtype and len(subtype.split(':')) == 2 and subtype.split(':')[1].strip() != '' and subtype.split(':')[1].strip().lower() != "none"}
        self.yellow_other_uncaught = copy.deepcopy(self.yellow_other_const)


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