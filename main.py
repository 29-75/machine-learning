from race import game

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

if __name__ == "__main__":
    # Declare game
    race_game = game.Game(auto=True)

    # Run car in builded map
    race_game.run_car()
