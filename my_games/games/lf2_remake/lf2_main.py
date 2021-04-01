# AngelStreet @2021
####################################################
import pygame as pg
from engine.src.game import Game, LAYER_GAME, LAYER_UI, LAYER_BG, BLACK
from lf2_game_menu import *
from lf2_game import LF2_Game

FPS = 60
GAME_WIDTH, GAME_HEIGHT = 1200, 600
TITLE = "Little Fighter 2 - Remake"
TILE_MAP_W, TILE_MAP_H = 175, 74
TILE_MAP = [[[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]


def scroll_bg(game, dir, max_scroll_x):
    if dir != 0:
        if dir < 0:
            if max_scroll_x['max_left']+dir > max_scroll_x['current']:
                return
        elif dir > 0:
            if max_scroll_x['max_right']+dir < max_scroll_x['current']:
                return
        max_scroll_x['current'] += dir
        for bg in game.bg_list:
            if not bg.x == 0:
                bg.image.fill(BLACK)
            rx = bg.x % bg.w
            #print(bg.x, max_scroll_x)
            bg.image.blit(bg.copy, (rx-bg.w, 0))
            if rx < bg.w:
                bg.image.blit(bg.copy, (rx, 0))
            bg.x += bg.speed*dir

def create_ennemies(game) :
    pass

def create_player(game):
    pass

def create_gamebar(game):
    p = 'assets/image/gbar/'
    img_list = [p+'avatar.png',p+'bg_img.png',p+'hp_bar.png',p+'mp_bar.png']
    game.add_imagegamebar(LAYER_UI,20,20,100, 100, *img_list, 0, 0.5)

def create_map(game):
    p = 'assets/image/lf/'
    l1, l2, l3, l4 = p+'land1.bmp', p+'land2.bmp', p+'land3.bmp', p+'land4.bmp'
    game.bg_5 = game.add_tiles_bg(LAYER_BG, 0, 230, TILE_MAP_W, TILE_MAP_H,
                                  [l1, l2, l3, l4], TILE_MAP, (0, 0, 0))
    game.bg_1 = game.add_parallax_bg(LAYER_BG, 0, 0, p+'forests.bmp', None, True)
    game.bg_2 = game.add_parallax_bg(LAYER_BG, 0, 15, p+'forestm1.bmp',  (0, 0, 0), True)
    #game.bg_3 = game.add_image(LAYER_BG, 0, 50, p+'forestm3.bmp',  None, (0, 0, 0))
    game.bg_4 = game.add_parallax_bg(LAYER_BG, 0, 80, p+'forestt.bmp',  (0, 0, 0))
    game.bg_list = [game.bg_2, game.bg_4, game.bg_5]
    game.bg_2.copy = game.bg_2.image.copy()
    game.bg_4.copy = game.bg_4.image.copy()
    game.bg_5.copy = game.bg_5.image.copy()
    game.bg_2.x, game.bg_2.speed = 0, 0.5
    game.bg_4.x, game.bg_4.speed = 0, 2
    game.bg_5.x, game.bg_5.speed = 0, 2

def create_menu(game):
    game_menu = GameMenu(GAME_WIDTH, GAME_HEIGHT, game)
    game.add_sprite(LAYER_UI, 0, 0, game_menu)
    game_menu.add('firstscreen', FirstScreenMenu(game_menu, 'assets/image/start_screen.png'))
    game_menu.add('loading_menu', LoadingMenu(game_menu, 'assets/image/loading_screen.png'))
    game_menu.add('main_menu', MainMenu(game_menu, 'assets/image/menu_screen.png'))
    game_menu.add('options_menu', OptionsMenu(game_menu))
    game_menu.add('credits_menu', CreditsMenu(game_menu))
    game_menu.add('game_options_menu', GameOptionsMenu(game_menu))
    game_menu.show('firstscreen')
    return game_menu

def launch_game(game, game_menu):
    game_menu.kill()
    game_menu = None
    pg.mixer.music.fadeout(300)
    create_map(game)

def main():
    # INIT pg----------------------
    pg.mixer.pre_init(44100, -16, 2, 512)
    pg.init()  # initiates pg
    pg.mixer.init()
    pg.display.set_caption(TITLE)
    display = pg.display.set_mode((GAME_WIDTH, GAME_HEIGHT), 0, 32)
    pg.mixer.music.load('assets/sound/lf2_theme_song.mp3')
    pg.mixer.music.set_volume(0.5)
    pg.mixer.music.play(-1)

    # GAME ---------------------
    game = LF2_Game(display, GAME_WIDTH, GAME_HEIGHT)
    #game_menu = create_menu(game)
    create_map(game)
    game_bar = create_gamebar(game)

    # LOOP----------------------
    running = True
    speed = 0
    max_scroll_x = {'current': 0, 'max_left': -1000, 'max_right': 0}
    clock = pg.time.Clock()
    while running:
        scroll_bg(game, speed, max_scroll_x)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.mixer.music.stop()
                return pg.quit()
            if event.type == LAUNCH_GAME:
                print(event.message)
                launch_game(game, game_menu)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if game_menu and not game_menu.current_menu:
                        game.resize_screen(game.w, game.h)
                        game_menu.show('game_options_menu')
                    else:
                        game_menu.current_menu.go_back()
                elif event.key == pg.K_RETURN:
                    if game_menu.current_menu:
                        game_menu.current_menu.press_enter()
                elif event.key == pg.K_BACKSPACE:
                    if game_menu:
                        game_menu.current_menu.go_back()
                    else:
                        game.move_sprite()
                elif event.key == pg.K_DOWN:
                    if game_menu:
                        game_menu.current_menu.move_cursor_down()
                elif event.key == pg.K_UP:
                    if game_menu:
                        game_menu.current_menu.move_cursor_up()
                elif event.key == pg.K_RIGHT:
                    if game.bg_list:
                        speed = -1
                elif event.key == pg.K_LEFT:
                    if game.bg_list:
                        speed = 1
            elif event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                    speed = 0

        game.draw()
        clock.tick(FPS)
        pg.display.update()


if __name__ == "__main__":
    main()
