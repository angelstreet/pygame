#AngelStreet @2021
####################################################
import pygame
from tilemap import draw_map
WHITE = (255, 255, 255)
RED = (255, 0, 0)
MAPOFFSETX, MAPOFFSETY = 300, 100

# FUNCTIONS----------------------
def draw_window():
    pygame.display.update()

# MAIN-------------------------
def main():
    # VAR----------------------
    MENU_WIDTH, MENU_HEIGHT = 1200, 800
    FPS = 60
    TITLE = "Isomap"
    # INIT PYGAME----------------------
    pygame.init()  # initiates pygame
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
    display = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
    # GAME ---------------------
    draw_map(screen, display)
    #draw_player(screen, display)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
