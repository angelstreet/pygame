# AngelStreet @2021
####################################################
import pygame as pg
from engine.src.game import Game, FONT_NAME, BLACK,LAYER_BG,LAYER_GAME,LAYER_UI
FPS = 60
GAME_WIDTH, GAME_HEIGHT = 1200, 600
TITLE = 'HealthBar!'


def main():
    # INIT pg----------------------
    pg.init()
    pg.display.set_caption(TITLE)
    display = pg.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    # GAME----------------------
    game = Game(display, GAME_WIDTH, GAME_HEIGHT)
    colorgamebar = game.add_colorgamebar(LAYER_GAME,100, 100, 10, 10, 200, 40)
    imagegamebar = game.add_imagegamebar(LAYER_GAME,100, 100, 10, 120, '../assets/image/healthbar_bg.png',
                                                         '../assets/image/healthbar_fill.png', 85, 0.5)
    heartgamebar = game.add_heartgamebar(LAYER_GAME,6, 6, 10, 250, '../assets/data/heart.json', 0.2, 10)
    hptext = game.add_text(LAYER_UI,'HP', FONT_NAME, 20, BLACK, None, 0, -20, imagegamebar)
    fpstext = game.add_dynamic_text(LAYER_UI,'',FONT_NAME, 20, BLACK, None, GAME_WIDTH-70, 20)
    logo = game.add_image(LAYER_BG,400,100,'../assets/image/fortnite.jpg', False, None, 1)
    # LOOP----------------------
    running = True
    clock = pg.time.Clock()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                return pg.quit()
        game.draw()
        colorgamebar.value = max(1, colorgamebar.value-0.3)
        imagegamebar.value = max(0, imagegamebar.value-0.1)
        heartgamebar.value = max(0, heartgamebar.value-0.01)
        fpstext.text = str(int(clock.get_fps()))+" FPS"
        clock.tick(FPS)
        pg.display.update()


if __name__ == "__main__":
    main()
