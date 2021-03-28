# AngelStreet @2021
####################################################
import pygame
from engine.src.game import Game, FONT_NAME, BLACK,LAYER_GAME,LAYER_UI


FPS = 60
GAME_WIDTH, GAME_HEIGHT = 1200, 600
TITLE = "TileMap"
KEYBOARD = "AZERTY"


def get_keyboard_keys():
    if KEYBOARD == "AZERTY":
        return pygame.K_q, pygame.K_d, pygame.K_z, pygame.K_s
    return pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s


def main():
    # INIT PYGAME----------------------
    pygame.init()  # initiates pygame
    pygame.display.set_caption(TITLE)
    display = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    # GAME ---------------------
    game = Game(display, GAME_WIDTH, GAME_HEIGHT)
    # game.image.fill(GREEN)
    fpstext = game.add_dynamic_text(LAYER_UI,'', FONT_NAME, 20, BLACK, None, GAME_WIDTH-70,
                                    20)
    tilemap = game.create_isotilemap(LAYER_GAME, '../assets/data/isotilemap.json', 0.5, True)
    player = game.create_isoplayer(LAYER_GAME, 530, 110, '../assets/data/isoplayer.json',
                                   tilemap.x, tilemap.y,
                                   tilemap.tile_w, tilemap.tile_h, 2)

    K_LEFT, K_RIGHT, K_UP, K_DOWN = get_keyboard_keys()
    # LOOP ---------------------
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == K_LEFT:
                    player.K_LEFT = True
                elif event.key == pygame.K_RIGHT or event.key == K_RIGHT:
                    player.K_RIGHT = True
                if event.key == pygame.K_UP or event.key == K_UP:
                    player.K_UP = True
                elif event.key == pygame.K_DOWN or event.key == K_DOWN:
                    player.K_DOWN = True
                if event.key == pygame.K_SPACE:
                    player.K_SPACE = True
                if event.key == pygame.K_RETURN:
                    player.K_RETURN = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == K_LEFT:
                    player.K_LEFT = False
                elif event.key == pygame.K_RIGHT or event.key == K_RIGHT:
                    player.K_RIGHT = False
                if event.key == pygame.K_UP or event.key == K_UP:
                    player.K_UP = False
                elif event.key == pygame.K_DOWN or event.key == K_DOWN:
                    player.K_DOWN = False
                if event.key == pygame.K_SPACE:
                    player.K_SPACE = False
                if event.key == pygame.K_RETURN:
                    player.K_RETURN = False
        fpstext.text = str(int(clock.get_fps()))+" FPS"
        game.draw()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
