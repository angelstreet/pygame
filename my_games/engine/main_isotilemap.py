#AngelStreet @2021
####################################################
import sys,os,pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.game import Game, GREEN,FONT_NAME,BLACK


FPS = 60
GAME_WIDTH, GAME_HEIGHT = 1200, 600
TITLE = "TileMap"
KEYBOARD = "AZERTY"

# FUNCTIONS----------------------
def get_keyboard_keys():
    if KEYBOARD=="AZERTY" :
        return pygame.K_q,pygame.K_d,pygame.K_z,pygame.K_s
    return pygame.K_a,pygame.K_d,pygame.K_w,pygame.K_s

def main():
    # INIT PYGAME----------------------
    pygame.init()  # initiates pygame
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    display = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
    # GAME ---------------------
    game = Game(screen, display, GAME_WIDTH, GAME_HEIGHT)
    #game.image.fill(GREEN)
    fpstext = game.add_dynamic_text('',FONT_NAME,20,BLACK,None, GAME_WIDTH-70,20, game.ui_sprites)
    #tilemap = game.create_isotilemap(0,100,1400,800,'assets/data/isotilemap.json',0.5)
    tilemap = game.create_isotilemap(600,100,1400,800,'assets/data/isotilemap.json',0.5, True)
    tilemap.game=game
    player = game.create_isoplayer('assets/data/isoplayer.json',tilemap.rect.x,tilemap.rect.y,tilemap.tile_w,tilemap.tile_h,2)
    player.move(530,100)
    K_LEFT, K_RIGHT,K_UP,K_DOWN = get_keyboard_keys()
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
        game.draw_screen()
        #game.check_collision()
        game.hide_sprites_for_player(player)
        clock.tick(FPS)

if __name__ == "__main__":
    main()
