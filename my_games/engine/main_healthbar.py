#AngelStreet @2021
####################################################
import sys,os,pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.game import Game,FONT_NAME,FONT_SIZE,BLACK
FPS = 60
GAME_WIDTH, GAME_HEIGHT = 1200, 600
TITLE = "HealthBar!"

def main():
    # INIT PYGAME----------------------
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    display = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
    # GAME----------------------
    game = Game(screen, display, GAME_WIDTH, GAME_HEIGHT)
    colorgamebar = game.create_colorgamebar(70, 100, 10, 10, 200, 40)
    imagegamebar = game.create_imagegamebar(80, 100, 10, 120,'assets/image/healthbar_bg.png','assets/image/healthbar_fill.png',84,0.5, (0,0,0))
    heartgamebar = game.create_heartgamebar(6, 6, 10, 250,'assets/data/heart.json',0.2,10)
    game.draw_text('HP', FONT_NAME,20,BLACK,100,110)
    # LOOP----------------------
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return pygame.quit()
        game.draw_screen(clock)
        colorgamebar.value=max(1,colorgamebar.value-0.3)
        imagegamebar.value=max(0,imagegamebar.value-0.2)
        heartgamebar.value=max(0,heartgamebar.value-0.01)
        clock.tick(FPS)

if __name__ == "__main__":
    main()
