#AngelStreet @2021
####################################################
import pygame
from tilemap import Map
from player import Player
MENU_WIDTH, MENU_HEIGHT = 1200, 800
FPS = 60
WHITE = (255, 255, 255)
TITLE = "Isomap"
MAP_X, MAP_Y = 250, 100
PLAYER_X, PLAYER_Y = 530,140
KEYBOARD = "AZERTY"

# FUNCTIONS----------------------
def get_keyboard_keys():
    if KEYBOARD=="AZERTY" :
        return pygame.K_q,pygame.K_d,pygame.K_z,pygame.K_s
    return pygame.K_a,pygame.K_d,pygame.K_w,pygame.K_s

def draw_game(screen,display,all_sprite,map):
    display.fill(WHITE)
    display.blit(map.image, (map.rect.x, map.rect.y))
    all_sprite.update()
    all_sprite.draw(display)
    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.update()

# MAIN-------------------------
def main():
    # INIT PYGAME----------------------
    pygame.init()  # initiates pygame
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
    display = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
    # GAME ---------------------
    map = Map('tilemap.json',0.5)
    map.move(MAP_X, MAP_Y)
    player = Player('player.json',2)
    player.move(PLAYER_X, PLAYER_Y)
    all_sprite = pygame.sprite.OrderedUpdates()
    all_sprite.add(player)
    running = True
    clock = pygame.time.Clock()
    K_LEFT, K_RIGHT,K_UP,K_DOWN = get_keyboard_keys()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return pygame.quit()
            if event.type == pygame.KEYDOWN:
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
            if event.type == pygame.KEYUP:
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

        draw_game(screen,display,all_sprite,map)
        clock.tick(FPS)


if __name__ == "__main__":
    main()
