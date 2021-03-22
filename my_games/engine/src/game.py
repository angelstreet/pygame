import pygame
from src.utility import FPS, WHITE, BLACK, draw_text, resize_screen
from src.ui import ColorGameBar,ImageGameBar,HeartGameBar
from src.isotilemap import IsoTileMap
from src.player import Player
from src.game_menu import GameMenu

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT_NAME = pygame.font.get_default_font()
FONT_SIZE = 14

class Game(pygame.sprite.Sprite):
    def __init__(self, screen, display, w, h, isplaying=True):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.display = display
        self.w, self.h = w, h
        self.mid_w, self.mid_h = w / 2, h / 2
        self.isplaying = isplaying
        self.init_game()

    def init_game(self):
        self.image = pygame.Surface((self.w, self.h))
        self.rect = self.image.get_rect()
        self.font_name = pygame.font.get_default_font()
        self.font_size = 20
        self.bg = pygame.Surface((self.w, self.h))
        self.fx = pygame.Surface((self.w, self.h))
        self.ui = pygame.Surface((self.w, self.h))
        self.bg_sprites = pygame.sprite.Group()
        self.game_sprites = pygame.sprite.OrderedUpdates()
        self.fx_sprites = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.OrderedUpdates()
        self.image.fill((255,255,255))
        self.bg_sprites.add(self)

#GAME-----------------------------------------------------
    def resize_screen(self,w,h,resizable=False):
        self.screen, self.display = resize_screen(w,h,resizable)

    def draw_text(self,text, font_name=FONT_NAME, size=FONT_SIZE, color=BLACK, x=0, y=0):
        draw_text(self.image, text, font_name, size, color, x, y)
#PLAYER-----------------------------------------------------
    def create_game_menu(self,w,h,game):
         self.game_menu = GameMenu(w,h,game)
         self.ui_sprites.add(self.game_menu)
         return  self.game_menu
    def hide_game_menu(self):
         self.ui_sprites.remove(self.game_menu)

    def show_game_menu(self):
           self.ui_sprites.add( self.game_menu)
#PLAYER-----------------------------------------------------
    def create_player(self,json,scale):
         player = Player(json,scale)
         self.game_sprites.add(player)
         return player
#ISOTILEMAP-----------------------------------------------------
    def create_isotilemap(self,x,y, json,scale):
        isotilemap = IsoTileMap(x,y,json,scale)
        self.bg_sprites.add(isotilemap.getBackground())
        self.game_sprites.add(isotilemap.getTiles())
        return isotilemap
#HEALTHBAR-----------------------------------------------------
    def create_colorgamebar(self, value,total, x, y, w,h):
        colorgamebar =ColorGameBar(value,total, x, y, w,h)
        self.ui_sprites.add(colorgamebar)
        return colorgamebar

    def create_imagegamebar(self,value,total, x, y,bg_img,fill_img,fill_offset,scale,keycolor):
        imagegamebar =ImageGameBar(value,total, x, y,bg_img,fill_img,fill_offset,scale,keycolor)
        self.ui_sprites.add(imagegamebar)
        return imagegamebar

    def create_heartgamebar(self,value,total, x, y,json,scale,offset):
        healthbar =HeartGameBar(value,total, x, y,json,scale,offset)
        self.ui_sprites.add(healthbar)
        return healthbar

#GAME-----------------------------------------------------
    def draw_bg(self):
        self.display.fill(WHITE)
        self.bg_sprites.draw(self.display)

    def zsort(self, sprite):
        return sprite.zsort()

    def sortGameSprite(self, game_sprites):
        tmp = game_sprites.sprites()
        tmp.sort(key=self.zsort)
        return pygame.sprite.OrderedUpdates(tmp)

    def draw_game(self):
        self.game_sprites.update()
        self.game_sprites = self.sortGameSprite(self.game_sprites)
        self.game_sprites.draw(self.display)

    def display_fps(self,clock):
        fps = str(int(clock.get_fps()))+" fps"
        draw_text(self.display, fps, FONT_NAME, FONT_SIZE, BLACK, self.w-50, 20)

    def draw_fx(self):
        self.fx_sprites.update()
        self.fx_sprites.draw(self.display)

    def draw_ui(self, clock):
        self.display_fps(clock)
        self.ui_sprites.update()
        self.ui_sprites.draw(self.display)


    def draw_screen(self,clock):
        self.draw_bg()
        if self.isplaying :
            self.draw_game()
            self.draw_fx()
        self.draw_ui(clock)
        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
        pygame.display.update()

    def resume(self):
        self.isplaying = True
        self.resize_screen(self.w,self.h,True)
