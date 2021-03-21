#AngelStreet @2021
####################################################
import sys,os,pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.game import Game
from src.game_menu import GameMenu
FPS = 60
GAME_WIDTH, GAME_HEIGHT = 1200, 600
TITLE = "Menu Interface!"

def main():
    # INIT PYGAME----------------------
    pygame.init()  # initiates pygame
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    display = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
    # INIT MENU----------------------
    game = Game(screen, display, GAME_WIDTH, GAME_HEIGHT)
    menuList = GameMenu(screen, display, GAME_WIDTH, GAME_HEIGHT, game)
    # LOOP----------------------
    clock = pygame.time.Clock()
    while True:
        game.check_events()
        game.draw_screen(clock)
        clock.tick(FPS)

if __name__ == "__main__":
    main()
