#AngelStreet @2021
####################################################
import sys,os,pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.game import Game, GREEN,FONT_NAME,BLACK


FPS = 60
GAME_WIDTH, GAME_HEIGHT = 1200, 600
TITLE = "TileMap A*"


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
    tilemap = game.create_isotilemap(-50,100,1400,800,'assets/data/isotilemap2.json',0.5)
    tilemap.game=game
    # LOOP ---------------------
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return pygame.quit()
        fpstext.text = str(int(clock.get_fps()))+" FPS"
        game.draw_screen()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
