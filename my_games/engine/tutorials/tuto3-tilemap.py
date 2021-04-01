# AngelStreet @2021
####################################################
import pygame as pg
from engine.src.game import Game, FONT_NAME, BLACK, LAYER_GAME, LAYER_UI,LAYER_TILEMAP


FPS = 60
GAME_WIDTH, GAME_HEIGHT = 1200, 600
TITLE = "TileMap"
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
    fpstext = game.add_dynamic_text(LAYER_UI,GAME_WIDTH-70, 20, '', FONT_NAME, 20, BLACK, None,
                                    )
    tilemap = game.add_tilemap(LAYER_TILEMAP, '../assets/data/tilemap.json', 1, True)
    # LOOP ---------------------
    running = True
    clock = pg.time.Clock()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                return pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                    return pg.quit()

        fpstext.text = str(int(clock.get_fps()))+" FPS"
        game.draw()
        clock.tick(FPS)
        pg.display.update()


if __name__ == "__main__":
    main()
