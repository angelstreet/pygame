import pygame
from src.utility import FPS, WHITE, BLACK, resize_screen
from src.ui import ColorGameBar, ImageGameBar, HeartGameBar
from src.isotilemap import IsoTileMap
from src.isoplayer import IsoPlayer
from src.game_menu import GameMenu
from src.game_objects import *
from pygame.locals import Color

FPS = 60
BLACK =Color('black')
WHITE = Color('white')
RED = Color('red')
GREEN = Color('green')
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
        # 4 layers bg, fx, game, ui ----------------------------
        self.bg = pygame.Surface((self.w, self.h))
        self.fx = pygame.Surface((self.w, self.h))
        self.ui = pygame.Surface((self.w, self.h))
        self.bg_sprites = pygame.sprite.OrderedUpdates()
        self.game_sprites = pygame.sprite.OrderedUpdates()
        self.fx_sprites = pygame.sprite.OrderedUpdates()
        self.ui_sprites = pygame.sprite.OrderedUpdates()
        # ------------------------------------------------------
        self.image.fill((255, 255, 255))
        self.bg_sprites.add(self)
        self.hided_sprites = []

# GAME-----------------------------------------------------
    def resize_screen(self, w, h, resizable=False):
        self.screen, self.display = resize_screen(w, h, resizable)

    def add_text(self, text, font_name, size, color, bg_color, x, y, layer, sprite=None, behind=False):
        text = Text(text, font_name, size, color, bg_color, x, y, layer, sprite, behind)
        return text

    def add_dynamic_text(self, text, font_name, size, color, bg_color, x, y, layer, sprite=None, behind=False):
        text = DynamicText(text, font_name, size, color, bg_color, x, y, layer, sprite, behind)
        return text

    def add_image(self, img_path,alpha, colorkey, x, y, scale, layer, sprite=None, behind=False):
        img = Image(img_path, alpha,colorkey, x, y, scale, layer, sprite, behind)
        return img

# PLAYER-----------------------------------------------------
    def create_game_menu(self, w, h, game):
        self.game_menu = GameMenu(w, h, game)
        self.ui_sprites.add(self.game_menu)
        return self.game_menu

    def hide_game_menu(self):
        self.ui_sprites.remove(self.game_menu)

    def show_game_menu(self):
        self.ui_sprites.add(self.game_menu)
# ISOPLAYER-----------------------------------------------------

    def create_isoplayer(self, json, map_x,map_y,tile_w,tile_h,scale=1):
        isoplayer = IsoPlayer(json, map_x,map_y,tile_w,tile_h,scale)
        self.game_sprites.add(isoplayer)
        return isoplayer
# ISOTILEMAP-----------------------------------------------------

    def create_isotilemap(self, map_w, map_h,x, y, json, scale, debug = False):
        isotilemap = IsoTileMap(map_w, map_h,x, y, json, scale,debug)
        self.bg_sprites.add(isotilemap.getBackground())
        self.game_sprites.add(isotilemap.getTiles())
        return isotilemap
# HEALTHBAR-----------------------------------------------------

    def create_colorgamebar(self, value, total, x, y, w, h):
        colorgamebar = ColorGameBar(value, total, x, y, w, h)
        self.ui_sprites.add(colorgamebar)
        return colorgamebar

    def create_imagegamebar(self, value, total, x, y, bg_img, fill_img, fill_offset, scale, alpha=True,keycolor=False):
        imagegamebar = ImageGameBar(value, total, x, y, bg_img,fill_img, fill_offset, scale,alpha, keycolor)
        self.ui_sprites.add(imagegamebar)
        return imagegamebar

    def create_heartgamebar(self, value, total, x, y, json, scale, offset):
        healthbar = HeartGameBar(value, total, x, y, json, scale, offset)
        self.ui_sprites.add(healthbar)
        return healthbar
# COLLISION-----------------------------------------------------
    def check_collision(self):
        moving_list = []
        non_moving_list = pygame.sprite.Group()

        for sprite in self.game_sprites.sprites() :
            if 'rigid' in dir(sprite) and sprite.rigid :
                if 'is_moving' in dir(sprite) and sprite.is_moving() :
                    moving_list.append(sprite.get_collision_sprite())
                else :
                    non_moving_list.add(sprite.get_collision_sprite())

        for collision_sprite in moving_list :
            #Side collision between 2 losange at z=0
            collision_list = pygame.sprite.spritecollide(collision_sprite, non_moving_list, False, pygame.sprite.collide_mask)
            for sprite in collision_list:
                #Z collision
                #print (sprite.parent.z,sprite.parent.offsety,collision_sprite.parent.z,collision_sprite.parent.rect.height)
                if sprite.parent.z<=collision_sprite.parent.z and sprite.parent.z>=collision_sprite.parent.z-collision_sprite.parent.rect.height:
                    collision_sprite.parent.collision_list.append(sprite)
                if sprite.parent.z-sprite.parent.rect.height<=collision_sprite.parent.z and sprite.parent.z>=collision_sprite.parent.z-collision_sprite.parent.rect.height:
                    collision_sprite.parent.collision_list.append(sprite)


# GAME-----------------------------------------------------
    def hide_sprites_for_player(self,player):
        for sprite in self.hided_sprites :
            sprite.image.blit(sprite.copy,(0,0))
        sprites = self.game_sprites.sprites().copy()
        sprites.remove(player)
        collision_list = pygame.sprite.spritecollide(player, sprites, False, pygame.sprite.collide_mask)
        player.mask = pygame.mask.from_surface(player.image)
        for sprite in collision_list:
            sprite.image.blit(sprite.copy,(0,0))

            if 'zsort' in dir(sprite) and player.zsort()<sprite.zsort():
                #print("zsort----------------")
                #print(player.rect.y,player.rect.height, player.z, player.zsort())
                #print(sprite.rect.y, sprite.rect.height,sprite.z, sprite.offsety, sprite.zsort())
                sprite.image.fill((255, 0, 0, 220), None, pygame.BLEND_RGBA_MULT)
                self.hided_sprites.append(sprite)
    def draw_bg(self):
        self.display.fill(WHITE)
        self.bg_sprites.draw(self.display)

    def zsort(self, sprite):
        if 'zsort' in dir(sprite):
            return sprite.zsort()
        return 1

    def sort_game_sprite(self, game_sprites):
        tmp = game_sprites.sprites()
        tmp.sort(key=self.zsort)
        return pygame.sprite.OrderedUpdates(tmp)

    def draw_game(self):
        self.game_sprites.update()
        self.check_collision()
        self.game_sprites = self.sort_game_sprite(self.game_sprites)

        self.game_sprites.draw(self.display)

    def draw_fx(self):
        self.fx_sprites.update()
        self.fx_sprites.draw(self.display)

    def draw_ui(self):
        self.ui_sprites.update()
        self.ui_sprites.draw(self.display)

    def draw_screen(self):
        self.draw_bg()
        if self.isplaying:
            self.draw_game()
            self.draw_fx()
        self.draw_ui()
        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
        pygame.display.update()

    def resume(self):
        self.isplaying = True
        self.resize_screen(self.w, self.h, True)
