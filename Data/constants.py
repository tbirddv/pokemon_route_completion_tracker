from enum import Enum

class SupportedGames(Enum):
    RED = 'Red'
    BLUE = 'Blue'
    YELLOW = 'Yellow'

Generation_1 = [SupportedGames.RED, SupportedGames.BLUE, SupportedGames.YELLOW]

generation_1_encounter_column_name_mappings = {
    SupportedGames.RED: {
        'walking': 'Red Walking',
        'surfing': 'Red Surfing',
        'fishing': 'Red Fishing',
        'other': 'Red Other',
    },
    SupportedGames.BLUE: {
        'walking': 'Blue Walking',
        'surfing': 'Blue Surfing',
        'fishing': 'Blue Fishing',
        'other': 'Blue Other',
    },
    SupportedGames.YELLOW: {
        'walking': 'Yellow Walking',
        'surfing': 'Yellow Surfing',
        'fishing': 'Yellow Fishing',
        'other': 'Yellow Other',
    }
}

generation_1_location_column_name_mappings = {
    SupportedGames.RED: ['Red Routes', 'Red Uniques'],
    SupportedGames.BLUE: ['Blue Routes', 'Blue Uniques'],
    SupportedGames.YELLOW: ['Yellow Routes', 'Yellow Uniques']
}

complex_evolutions = {
    'gen_1': ['eevee']
}
