#AngelStreet @2021
####################################################
import sys,os,pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game_menu import GameMenu
from game import Game

# MAIN-------------------------
def main():
    # VAR----------------------
    MENU_WIDTH, MENU_HEIGHT = 900, 500
    GAME_WIDTH, GAME_HEIGHT = 1200, 600
    TITLE = "First Game!"
    # INIT PYGAME----------------------
    pygame.init()  # initiates pygame
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
    display = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
    # INIT MENU----------------------
    game = Game(screen, display, GAME_WIDTH, GAME_HEIGHT)
    menuList = GameMenu(screen, display, MENU_WIDTH, MENU_HEIGHT, game)


if __name__ == "__main__":
    main()
