class Pokemon:
    def __init__(self, name, id, status="Uncaught"):
        self.name = name
        self.id = id
        self.status = status

    def to_dict(self):
        return {
            'name': self.name,
            'id': self.id,
            'status': self.status
        }

class Local_Gen1(Pokemon):
    def __init__(self, name, id, red_locations, blue_locations, yellow_locations, devolutions, evolutions, status="Uncaught"):
        super().__init__(name, id, status)
        self.red_locations = red_locations
        self.blue_locations = blue_locations
        self.yellow_locations = yellow_locations
        self.devolutions = devolutions
        self.evolutions = evolutions
    
    @classmethod
    def from_csv(cls, row):
        name = row['Name']
        id = int(row['ID'])
        red_locations = [f"Route {route.strip()}" for route in row['Red Routes'].strip().split('/') if route.strip() != '' and route.strip().lower() != "none"] + [unique.strip() for unique in row['Red Uniques'].strip().split('/') if unique.strip() != '' and unique.strip().lower() != "none"]
        blue_locations = [f"Route {route.strip()}" for route in row['Blue Routes'].strip().split('/') if route.strip() != '' and route.strip().lower() != "none"] + [unique.strip() for unique in row['Blue Uniques'].strip().split('/') if unique.strip() != '' and unique.strip().lower() != "none"]
        yellow_locations = [f"Route {route.strip()}" for route in row['Yellow Routes'].strip().split('/') if route.strip() != '' and route.strip().lower() != "none"] + [unique.strip() for unique in row['Yellow Uniques'].strip().split('/') if unique.strip() != '' and unique.strip().lower() != "none"]
        devolutions = [pokemon.strip() for pokemon in row['Devolutions'].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
        evolutions = [pokemon.strip() for pokemon in row['Evolutions'].strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
        return cls(name, id, red_locations, blue_locations, yellow_locations, devolutions, evolutions)
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            id=data['id'],
            red_locations=data.get('red_locations', []),
            blue_locations=data.get('blue_locations', []),
            yellow_locations=data.get('yellow_locations', []),
            devolutions=data.get('devolutions', []),
            evolutions=data.get('evolutions', []),
            status=data.get('status', 'Uncaught')
        )


    def __repr__(self):
        lines = [f"Gen1 Pokemon ID: {self.id}, Name: {self.name}, Status: {self.status}"]
        
        if self.red_locations:
            lines.append(f"Red Locations: {self.red_locations}")
        if self.blue_locations:
            lines.append(f"Blue Locations: {self.blue_locations}")
        if self.yellow_locations:
            lines.append(f"Yellow Locations: {self.yellow_locations}")
        if self.devolutions:
            lines.append(f"Devolutions: {self.devolutions}")
        if self.evolutions:
            lines.append(f"Evolutions: {self.evolutions}")
        
        return ",\n".join(lines)
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'red_locations': self.red_locations,
            'blue_locations': self.blue_locations,
            'yellow_locations': self.yellow_locations,
            'devolutions': self.devolutions,
            'evolutions': self.evolutions
        })
        return base_dict