from race import game

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

if __name__ == "__main__":
    race_game = game.Game(1280, 720, auto=False)

    print(f'')
    race_game.run()
