# AngelStreet @2021
####################################################
import pygame as pg
from engine.src.game import Game, FONT_NAME, BLACK, LAYER_GAME, LAYER_UI, LAYER_TILEMAP
from engine.src.tile import Tile


FPS = 60
GAME_WIDTH, GAME_HEIGHT = 1200, 600
TITLE = "TileMap Pathfinding"


def sort(sprite):
    return sprite.zsort()


def main():
    # INIT PYGAME----------------------
    pg.init()  # initiates pygame
    pg.display.set_caption(TITLE)
    display = pg.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    # GAME ---------------------
    game = Game(display, GAME_WIDTH, GAME_HEIGHT)
    fpstext = game.add_dynamic_text(LAYER_UI, GAME_WIDTH-70, 20, 'FPS', FONT_NAME, 20, BLACK, None)
    pathtext = game.add_dynamic_text(LAYER_UI, 50, 20, 'Path', FONT_NAME, 20, BLACK, None)
    tilemap = game.add_isotilemap(LAYER_TILEMAP, '../assets/data/isotilemap.json', 0.5)
    tilemap.game = game
    # LOOP ---------------------
    running = True
    clock = pg.time.Clock()
    src = None
    dst = None
    paths = []
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                return pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if src and dst:
                    src.remove_blend()
                    dst.remove_blend()
                    src, dst = None, None
                    for i in range(0, 3):
                        if i < len(paths):
                            for tile in paths[i]:
                                tile.remove_blend()
                else:
                    sprite_list = []
                    pos = pg.mouse.get_pos()
                    for sprite in game.game_sprites.sprites():
                        pos_in_mask = pos[0] - sprite.rect.x, pos[1] - sprite.rect.y
                        if isinstance(sprite, Tile) and sprite.rect.collidepoint(pos) and sprite.mask.get_at(pos_in_mask):
                            sprite_list.append(sprite)
                    if len(sprite_list) > 0:
                        sprite_list.sort(key=sort)
                        if not src:
                            src = sprite_list[-1]
                            src.blend((255, 0, 0, 255))
                        elif not dst:
                            dst = sprite_list[-1]
                            dst.blend((0, 0, 255, 255))
                            paths, score = tilemap.get_path(src, dst)

                            for i in range(0, 3):
                                if i < len(paths):
                                    pathtext.text = 'Best path found with score: %s' % score
                                    for tile in paths[i]:
                                        tile.blend((255, 0, 0, 255))
                                    game.draw()
                                    pg.display.update()
                                    pg.time.delay(500)
                                    if i < min(2, len(paths)-1):
                                        for tile in paths[i]:
                                            tile.remove_blend()
                                elif not paths:
                                    pathtext.text = "No path found"

        fpstext.text = str(int(clock.get_fps()))+" FPS"
        game.draw()
        clock.tick(FPS)
        pg.display.update()


if __name__ == "__main__":
    main()
