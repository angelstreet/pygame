#AngelStreet @2021
####################################################
import sys,os,pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.game import Game, GREEN,FONT_NAME,BLACK


FPS = 60
GAME_WIDTH, GAME_HEIGHT = 1200, 600
TITLE = "TileMap A*"

def sort(sprite):
    return sprite.zsort()

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
    mouseclicktext = game.add_dynamic_text('',FONT_NAME,20,BLACK,None, 50,20, game.ui_sprites)
    #tilemap = game.create_isotilemap(0,100,1400,800,'assets/data/isotilemap.json',0.5)
    tilemap = game.create_isotilemap(600,100,1400,800,'assets/data/isotilemap2.json',0.5)
    tilemap.game=game
    # LOOP ---------------------
    running = True
    clock = pygame.time.Clock()
    src = None
    dst = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if src and dst :
                    print("Clean path")
                    src.image.blit(sprite.copy,(0 ,0))
                    dst.image.blit(sprite.copy,(0 ,0))
                    src , dst = None , None
                else:
                    sprite_list=[]
                    pos = pygame.mouse.get_pos()
                    for sprite in game.game_sprites.sprites():
                        pos_in_mask = pos[0] - sprite.rect.x, pos[1] - sprite.rect.y
                        if sprite.rect.collidepoint(pos) and sprite.mask.get_at(pos_in_mask):
                            sprite_list.append(sprite)
                    if len(sprite_list)>0 :
                        sprite_list.sort(key=sort)
                        if not src :
                            src = sprite_list[-1]
                            #print("Src",src.i,src.j)
                            src.image.fill((255, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
                        elif not dst :
                            dst = sprite_list[-1]
                            #print("Dst",dst.i,dst.j)
                            dst.image.fill((0, 0, 255, 255), None, pygame.BLEND_RGBA_MULT)
                            path = tilemap.get_path(src,dst)


        fpstext.text = str(int(clock.get_fps()))+" FPS"
        game.draw_screen()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
