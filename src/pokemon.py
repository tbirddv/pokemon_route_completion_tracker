class Pokemon:
    def __init__(self, name, id, status="Uncaught"):
        self.name = name
        self.id = id
        self.status = status

class Local_Gen1(Pokemon):
    def __init__(self, name, id, red_routes, red_uniques, blue_routes, blue_uniques, yellow_routes, yellow_uniques, devolutions, evolutions):
        super().__init__(name, id)
        self.red_locations = [f"Route {route.strip()}" for route in red_routes.strip().split('/') if route.strip() != '' and route.strip().lower() != "none"] + [unique.strip() for unique in red_uniques.strip().split('/') if unique.strip() != '' and unique.strip().lower() != "none"]
        self.blue_locations = [f"Route {route.strip()}" for route in blue_routes.strip().split('/') if route.strip() != '' and route.strip().lower() != "none"] + [unique.strip() for unique in blue_uniques.strip().split('/') if unique.strip() != '' and unique.strip().lower() != "none"]
        self.yellow_locations = [f"Route {route.strip()}" for route in yellow_routes.strip().split('/') if route.strip() != '' and route.strip().lower() != "none"] + [unique.strip() for unique in yellow_uniques.strip().split('/') if unique.strip() != '' and unique.strip().lower() != "none"]
        self.devolutions = [pokemon.strip() for pokemon in devolutions.strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
        self.evolutions = [pokemon.strip() for pokemon in evolutions.strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]


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