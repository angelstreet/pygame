# AngelStreet @2021
####################################################
import pygame
from engine.src.game import Game, LAYER_GAME, LAYER_UI
from engine.src.game_menu import FirstScreenMenu, LoadingMenu, MainMenu, OptionsMenu, CreditsMenu, GameOptionsMenu

FPS = 60
GAME_WIDTH, GAME_HEIGHT = 1200, 675
TITLE = "Menu Interface!"


def main():
    # INIT PYGAME----------------------
    pygame.init()  # initiates pygame
    pygame.display.set_caption(TITLE)
    display = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    # GAME ---------------------
    game = Game(display, GAME_WIDTH, GAME_HEIGHT)
    game_menu = game.create_game_menu(LAYER_UI, GAME_WIDTH, GAME_HEIGHT, game)
    game_menu.add('firstscreen', FirstScreenMenu(game_menu, '../assets/image/fortnite.jpg'))
    game_menu.add('loading_menu', LoadingMenu(game_menu, '../assets/image/fortnite_loading.jpg',
                              '../assets/sound/fortnite_loading.mp3'))
    game_menu.add('main_menu', MainMenu(game_menu))
    game_menu.add('options_menu', OptionsMenu(game_menu))
    game_menu.add('credits_menu', CreditsMenu(game_menu))
    game_menu.add('game_options_menu', GameOptionsMenu(game_menu))
    game_menu.show('main_menu')

    # LOOP----------------------
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.music.stop()
                return pygame.quit()
            if event.type == pygame.VIDEORESIZE:
                game.w, game.h = event.w, event.h
                game.mid_w, game.mid_h = game.w / 2, game.h / 2
                game.resize_screen(event.w, event.h, True)
            # LISTEN GAME MENU KEY EVENT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not game_menu.current_menu:
                        game.resize_screen(game.w, game.h)
                        game_menu.show('game_options_menu')
                    else:
                        game_menu.current_menu.go_back()
                elif event.key == pygame.K_RETURN:
                    game_menu.current_menu.press_enter()
                elif event.key == pygame.K_BACKSPACE:
                    game_menu.current_menu.go_back()
                elif event.key == pygame.K_DOWN:
                    game_menu.current_menu.move_cursor_down()
                elif event.key == pygame.K_UP:
                    game_menu.current_menu.move_cursor_up()
        game.draw()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
