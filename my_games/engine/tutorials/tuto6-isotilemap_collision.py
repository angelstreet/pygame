# AngelStreet @2021
####################################################
import pygame as pg
from engine.src.game import Game, FONT_NAME, BLACK, LAYER_UI, LAYER_TILEMAP

FPS = 60
GAME_WIDTH, GAME_HEIGHT = 1200, 600
TITLE = "TileMap Collision"
KEYBOARD = "AZERTY"


def get_keyboard_keys():
    if KEYBOARD == "AZERTY":
        return pg.K_q, pg.K_d, pg.K_z, pg.K_s
    return pg.K_a, pg.K_d, pg.K_w, pg.K_s


def main():
    # INIT pg----------------------
    pg.init()  # initiates pg
    pg.display.set_caption(TITLE)
    display = pg.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    # GAME ---------------------
    game = Game(display, GAME_WIDTH, GAME_HEIGHT)
    fpstext = game.add_dynamic_text(LAYER_UI, GAME_WIDTH-70, 20, '', FONT_NAME, 20, BLACK, None)
    tilemap = game.add_isotilemap(LAYER_TILEMAP, '../assets/data/isotilemap.json', 0.5)
    player = game.add_4D_iso_player(LAYER_TILEMAP, 380, 120, '../assets/data/isoplayer.json', 2)
    player.set_tilemap(tilemap.x, tilemap.y, tilemap.tile_w, tilemap.tile_h)
    player.debug = True
    K_LEFT, K_RIGHT, K_UP, K_DOWN = get_keyboard_keys()
    # LOOP ---------------------
    running = True
    clock = pg.time.Clock()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                return pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT or event.key == K_LEFT:
                    player.K_LEFT = True
                elif event.key == pg.K_RIGHT or event.key == K_RIGHT:
                    player.K_RIGHT = True
                if event.key == pg.K_UP or event.key == K_UP:
                    player.K_UP = True
                elif event.key == pg.K_DOWN or event.key == K_DOWN:
                    player.K_DOWN = True
                if event.key == pg.K_SPACE:
                    player.K_SPACE = True
                if event.key == pg.K_RETURN:
                    player.K_RETURN = True
            elif event.type == pg.KEYUP:
                if event.key == pg.K_LEFT or event.key == K_LEFT:
                    player.K_LEFT = False
                elif event.key == pg.K_RIGHT or event.key == K_RIGHT:
                    player.K_RIGHT = False
                if event.key == pg.K_UP or event.key == K_UP:
                    player.K_UP = False
                elif event.key == pg.K_DOWN or event.key == K_DOWN:
                    player.K_DOWN = False
                if event.key == pg.K_SPACE:
                    player.K_SPACE = False
                if event.key == pg.K_RETURN:
                    player.K_RETURN = False
        fpstext.text = str(int(clock.get_fps()))+" FPS"
        game.sort_player(player)
        game.check_player_collision(player)
        game.draw()
        clock.tick(FPS)
        pg.display.update()


if __name__ == "__main__":
    main()
