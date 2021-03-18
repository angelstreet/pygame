#AngelStreet @2021
####################################################
import pygame
from game_menu import GameMenu
from game1.game import Game


#FUNCTIONS----------------------
def draw_window():
    pygame.display.update()

#MAIN----------------------
def main():
    #VAR----------------------
    WIDTH, HEIGHT = 900, 500
    WINDOW_SIZE = (WIDTH, HEIGHT)
    TITLE = "First Game!"
    #INIT PYGAME----------------------
    pygame.init() # initiates pygame
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode(WINDOW_SIZE) # initiate the window
    display = pygame.Surface(WINDOW_SIZE) # used as the surface for rendering, which is scaled
    run = True
    #INIT MENU----------------------
    game = Game(screen,display,WIDTH,HEIGHT)
    menuList = GameMenu(screen,display,WIDTH,HEIGHT,game)
if __name__ == "__main__":
    main()
