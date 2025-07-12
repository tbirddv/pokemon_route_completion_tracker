from src.utils import (get_game_enum, SaveData, save_game_data, load_save_file)
from Data.constants import SupportedGames
from src.newgame import new_game

def main():
    new_game("red")
    save_data = load_save_file("red")
    save_data.settings.game = SupportedGames.BLUE
    save_game_data("red", save_data)


if __name__ == "__main__":
    main()
