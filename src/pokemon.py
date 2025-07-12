class Pokemon:
    def __init__(self, name, id, status="Uncaught"):
        self.name = name
        self.id = id
        self.status = status

class Local_Gen1(Pokemon):
    def __init__(self, name, id, red_routes, red_uniques, blue_routes, blue_uniques, yellow_routes, yellow_uniques, devolutions, evolutions, status="Uncaught"):
        super().__init__(name, id, status)
        self.red_locations = [f"Route {route.strip()}" for route in red_routes.strip().split('/') if route.strip() != '' and route.strip().lower() != "none"] + [unique.strip() for unique in red_uniques.strip().split('/') if unique.strip() != '' and unique.strip().lower() != "none"]
        self.blue_locations = [f"Route {route.strip()}" for route in blue_routes.strip().split('/') if route.strip() != '' and route.strip().lower() != "none"] + [unique.strip() for unique in blue_uniques.strip().split('/') if unique.strip() != '' and unique.strip().lower() != "none"]
        self.yellow_locations = [f"Route {route.strip()}" for route in yellow_routes.strip().split('/') if route.strip() != '' and route.strip().lower() != "none"] + [unique.strip() for unique in yellow_uniques.strip().split('/') if unique.strip() != '' and unique.strip().lower() != "none"]
        self.devolutions = [pokemon.strip() for pokemon in devolutions.strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]
        self.evolutions = [pokemon.strip() for pokemon in evolutions.strip().split('/') if pokemon.strip() != '' and pokemon.strip().lower() != "none"]