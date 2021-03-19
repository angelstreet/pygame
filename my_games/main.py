#AngelStreet @2021
####################################################
import pygame
from utility import resize_screen
from game_menu import GameMenu
from game1.game import Game


#FUNCTIONS----------------------
def draw_window():
    pygame.display.update()

#MAIN------------------""----
def main():
    #VAR----------------------
    MENU_WIDTH, MENU_HEIGHT = 900, 500
    GAME_WIDTH, GAME_HEIGHT = 1200, 600
    TITLE = "First Game!"
    #INIT PYGAME----------------------
    pygame.init() # initiates pygame
    pygame.display.set_caption(TITLE)
    screen,display = resize_screen(MENU_WIDTH, MENU_HEIGHT)
    run = True
    #INIT MENU----------------------
    game = Game(screen,display,GAME_WIDTH, GAME_HEIGHT)
    menuList = GameMenu(screen,display,MENU_WIDTH, MENU_HEIGHT,game)
if __name__ == "__main__":
    main()
