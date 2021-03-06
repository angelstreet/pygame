# AngelStreet @2021
####################################################
import pygame
from src.game import Game, FONT_NAME, BLACK, RED


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
    #game.image.fill(RED)
    fpstext = game.add_dynamic_text(3,'', FONT_NAME, 20, BLACK, None, GAME_WIDTH-70,
                                    20)
    tilemap = game.create_tilemap(2, '../assets/data/tilemap.json', 0.5, True)
    #game.image.blit(tilemap.tile_list['1']['image'], (0, 0))
    # LOOP ---------------------
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return pygame.quit()

        fpstext.text = str(int(clock.get_fps()))+" FPS"
        game.draw()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
