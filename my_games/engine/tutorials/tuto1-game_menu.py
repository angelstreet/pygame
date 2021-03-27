# AngelStreet @2021
####################################################
import pygame,sys
print(sys.path)
from engine.src.game import Game, LAYER_GAME, LAYER_UI
from engine.src.game_menu import FirstScreenMenu, LoadingMenu, MainMenu, OptionsMenu, CreditsMenu, GameOptionsMenu

FPS = 60
GAME_WIDTH, GAME_HEIGHT = 1200, 675
TITLE = "Menu Interface!"


def main():
    # INIT PYGAME----------------------
    pygame.init()  # initiates pygame
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    # GAME ---------------------
    game = Game(screen, GAME_WIDTH, GAME_HEIGHT, False)
    tilemap = game.create_isotilemap(LAYER_GAME, 600, 100, 1400, 800, '../assets/data/isotilemap.json', 0.5)
    game_menu = game.create_game_menu(LAYER_UI, GAME_WIDTH, GAME_HEIGHT, game)
    game_menu.first_screen_menu = FirstScreenMenu(LAYER_UI,game_menu, '../assets/image/fortnite.jpg')
    game_menu.loading_menu = LoadingMenu(LAYER_UI,
        game_menu, '../assets/image/fortnite_loading.jpg', '../assets/sound/fortnite_loading.mp3')
    game_menu.main_menu = MainMenu(LAYER_UI,game_menu)
    game_menu.options_menu = OptionsMenu(LAYER_UI,game_menu)
    game_menu.credits_menu = CreditsMenu(LAYER_UI,game_menu)
    game_menu.game_options_menu = GameOptionsMenu(LAYER_UI,game_menu)
    game_menu.current_menu = game_menu.first_screen_menu
    game_menu.current_menu.show()

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
                if game.isplaying:
                    if event.key == pygame.K_ESCAPE:
                        game.K_ESCAPE = True
                        game.isplaying = False
                        game.resize_screen(game.w, game.h)
                        game_menu.game_options_menu.show()
                        game.show_game_menu()
                else:
                    if event.key == pygame.K_ESCAPE:
                        game_menu.current_menu.go_back()
                    if event.key == pygame.K_RETURN:
                        game_menu.current_menu.press_enter()
                    if event.key == pygame.K_BACKSPACE:
                        game_menu.current_menu.go_back()
                    if event.key == pygame.K_DOWN:
                        game_menu.current_menu.move_cursor_down()
                    if event.key == pygame.K_UP:
                        game_menu.current_menu.move_cursor_up()
        game.draw()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
