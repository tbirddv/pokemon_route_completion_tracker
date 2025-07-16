from Data.constants import SupportedGames, generation_1_location_column_name_mappings

class Pokemon:
    def __init__(self, name, national_id, status="Uncaught"):
        self.name = name
        self.national_id = national_id
        self.status = status

    def to_dict(self):
        return {
            'name': self.name,
            'national_id': self.national_id,
            'status': self.status
        }

class Local_Gen1(Pokemon):
    def __init__(self, name, id, locations, devolutions, evolutions, status="Uncaught"):
        super().__init__(name, id, status)
        self.locations = locations
        self.devolutions = devolutions
        self.evolutions = evolutions
    
    @staticmethod
    def _process_location_fields(routes, uniques):
        return [f"Route {route.strip()}" for route in routes.strip().split('/') if route.strip() != '' and route.strip().lower() != "none"] + [unique.strip() for unique in uniques.strip().split('/') if unique.strip() != '' and unique.strip().lower() != "none"]
    
    @staticmethod
    def _process_evolution_field(evolution_str):
        return [pokemon.strip().lower() for pokemon in evolution_str.strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]

    @classmethod
    def from_csv(cls, row):
        name = row['Name'].lower()
        id = int(row['ID'])
        locations = {}
        for game, columns in generation_1_location_column_name_mappings.items():
            locations[game.value] = cls._process_location_fields(row[columns[0]], row[columns[1]])
        devolutions = cls._process_evolution_field(row['Devolutions'])
        evolutions = cls._process_evolution_field(row['Evolutions'])
        return cls(name, id, locations, devolutions, evolutions)

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            id=data['national_id'],
            locations=data.get('locations', {}),
            devolutions=data.get('devolutions', []),
            evolutions=data.get('evolutions', []),
            status=data.get('status', 'Uncaught')
        )

    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'locations': self.locations,
            'devolutions': self.devolutions,
            'evolutions': self.evolutions
        })
        return base_dict