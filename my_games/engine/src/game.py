import pygame as pg
from engine.src.utility import WHITE,BLACK,RED,GREEN, move_sprite
from engine.src.gamebar import ColorGameBar, ImageGameBar, HeartGameBar
from engine.src.tilemap import TileMap, IsoTileMap
from engine.src.player import HorizontalPlayer, VerticalPlayer, FourDirPlayer, FourDirIsoPlayer, HeightDirPlayer
from engine.src.game_menu import GameMenu
from engine.src.gametext import Text, DynamicText
from engine.src.button import Button
from engine.src.gamesprite import GameSprite

FPS = 60
FONT_NAME = pg.font.get_default_font()
FONT_SIZE = 14
LAYER_BG = 0
LAYER_TILEMAP = 1
LAYER_GAME = 99
LAYER_UI = 100


class Game(pg.sprite.Sprite):
    def __init__(self, display, w, h):
        pg.sprite.Sprite.__init__(self)
        self.display = display
        self.w, self.h = w, h
        self.mid_w, self.mid_h = w / 2, h / 2
        self.font_name = FONT_NAME
        self.font_size = FONT_SIZE
        self.game_sprites = pg.sprite.LayeredUpdates()
        self.hided_sprites = []
        self.image = pg.Surface(self.display.get_size(), pg.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()
        self.layer = LAYER_GAME
        self.game_sprites.add(self)
        self.display.fill(WHITE)

# GAME-----------------------------------------------------

    def resize_screen(self, w, h, resizable=False):
        if resizable:
            pg.display.set_mode((w, h), pg.RESIZABLE)
        else:
            pg.display.set_mode((w, h))

    def add_text(self, layer, text, font_name, size, color, bg_color, x, y, sprite=None):
        text = Text(text, font_name, size, color, bg_color, x, y, sprite)
        self.game_sprites.add(text, layer=layer)
        return text

    def add_dynamic_text(self, layer, text, font_name, size, color, bg_color, x, y, sprite=None):
        text = DynamicText(text, font_name, size, color, bg_color, x, y, sprite)
        self.game_sprites.add(text, layer=layer)
        return text

    def create_button(self, layer, x, y, w, h,  text, font_name, font_size, font_color, bg_color):
        btn = Button(w, h, text, font_name, font_size, font_color, bg_color)
        move_sprite(btn, x, y)
        self.game_sprites.add(btn, layer=layer)
        return btn

    def add_image(self, layer, img_path, alpha, colorkey, x, y, scale, sprite=None):
        img = GameSprite()
        img.load_image(img_path, alpha, colorkey, scale)
        img.move(x, y)
        self.game_sprites.add(img, layer=layer)
        return img

# MENU-----------------------------------------------------
    def create_game_menu(self, layer, w, h, game):
        self.game_menu = GameMenu(w, h, game)
        self.game_sprites.add(self.game_menu, layer=layer)
        return self.game_menu

    def hide_game_menu(self):
        self.game_sprites.remove(self.game_menu)

    def show_game_menu(self, layer):
        self.game_sprites.add(self.game_menu, layer=layer)

# ISOPLAYER-----------------------------------------------------
    def create_h_player(self, layer, x, y, json, scale=1, force_right=False):
        player = HorizontalPlayer(layer+2, json, scale, force_right)
        player.move(x, y)
        self.game_sprites.add(player)
        return player

    def create_v_player(self, layer, x, y, json, scale=1, force_up=False):
        player = VerticalPlayer(layer+2, json, scale, force_up)
        player.move(x, y)
        self.game_sprites.add(player)
        return player

    def create_4D_player(self, layer, x, y, json, scale=1):
        player = FourDirPlayer(layer+2, json, scale)
        player.move(x, y)
        self.game_sprites.add(player)
        return player

    def create_4D_iso_player(self, layer, x, y, json, scale=1):
        player = FourDirIsoPlayer(layer+2, json, scale)
        player.move(x, y)
        self.game_sprites.add(player)
        return player

    def create_8D_player(self, layer, x, y, json, scale=1, force_up=False):
        player = HeightDirPlayer(layer+2, json, scale)
        player.move(x, y)
        self.game_sprites.add(player)
        return player

    # @profile
    def sort_player(self, player):
        collision_list = []
        if player.is_moving():
            for sprite in self.hided_sprites:
                sprite.image.set_alpha(255)
            self.hided_sprites = []
            sprites = self.game_sprites.get_sprites_from_layer(player.layer)
            group = sprites.copy()
            group.remove(player)
            collision_list = pg.sprite.spritecollide(player, group, False, pg.sprite.collide_mask)
            centerx, centery = player.center()
            sprites.sort(key=lambda s: s.zsort())
            self.game_sprites.remove_sprites_of_layer(player.layer)
            self.game_sprites.add(sprites)
            index = sprites.index(player)
            for sprite in collision_list:
                if sprites.index(sprite) > index:
                    sprite.image.set_alpha(180)
                    self.hided_sprites.append(sprite)

    # @profile
    def check_player_collision(self, player):
        if player.is_moving():
            sprites, collision_list = [], []
            sprites = self.game_sprites.get_sprites_from_layer(player.layer)
            sprites.remove(player)
            if sprites:
                p = player.get_collision_sprite()
                for sprite in sprites:
                    collision_list.append(sprite.get_collision_sprite())
                collision_list = pg.sprite.spritecollide(
                    p, collision_list, False, pg.sprite.collide_mask)

                for sprite in collision_list:
                    # Side collision between 2 losange at z=0
                    # Z collision
                    if sprite.parent.z <= p.parent.z and sprite.parent.z >= p.parent.z-p.parent.rect.height:
                        p.parent.collision_list.append(sprite)
                    if sprite.parent.z-sprite.parent.rect.height <= p.parent.z and sprite.parent.z >= p.parent.z-p.parent.rect.height:
                        p.parent.collision_list.append(sprite)

    # def check_collision(self):
    #     moving_list = []
    #     non_moving_list = pg.sprite.Group()
    #     for sprite in self.game_sprites.sprites():
    #         if sprite.rigid:
    #             if sprite.is_moving():
    #                 moving_list.append(sprite.get_collision_sprite())
    #             else:
    #                 non_moving_list.add(sprite.get_collision_sprite())
    #     for collision_sprite in moving_list:
    #         # Side collision between 2 losange at z=0
    #         collision_list = pg.sprite.spritecollide(
    #             collision_sprite, non_moving_list, False, pg.sprite.collide_mask)
    #         for sprite in collision_list:
    #             # Z collision
    #             if sprite.parent.z <= collision_sprite.parent.z and sprite.parent.z >= collision_sprite.parent.z-collision_sprite.parent.rect.height:
    #                 collision_sprite.parent.collision_list.append(sprite)
    #             if sprite.parent.z-sprite.parent.rect.height <= collision_sprite.parent.z and sprite.parent.z >= collision_sprite.parent.z-collision_sprite.parent.rect.height:
    #                 collision_sprite.parent.collision_list.append(sprite)

# MAP-----------------------------------------------------

    def create_tilemap(self, layer, map_json, map_scale=1, debug=False):
        self.tilemap = TileMap(layer, map_json, map_scale, debug)
        self.game_sprites.add(self.tilemap.get_sprites())
        return self.tilemap

    def create_isotilemap(self, layer, map_json, map_scale=1, debug=False):
        self.isotilemap = IsoTileMap(layer, map_json, map_scale, debug)
        self.game_sprites.add(self.isotilemap.get_sprites())
        return self.isotilemap
# HEALTHBAR-----------------------------------------------------

    def create_colorgamebar(self, layer, value, total, x, y, w, h):
        colorgamebar = ColorGameBar(value, total, x, y, w, h)
        self.game_sprites.add(colorgamebar, layer=layer)
        return colorgamebar

    def create_imagegamebar(self, layer, value, total, x, y, bg_img, fill_img, fill_offset, scale, alpha=True, keycolor=False):
        imagegamebar = ImageGameBar(value, total, x, y, bg_img, fill_img,
                                    fill_offset, scale, alpha, keycolor)
        self.game_sprites.add(imagegamebar, layer=layer)
        return imagegamebar

    def create_heartgamebar(self, layer, value, total, x, y, json, scale, offset):
        healthbar = HeartGameBar(value, total, x, y, json, scale, offset)
        self.game_sprites.add(healthbar, layer=layer)
        return healthbar

# GAME-----------------------------------------------------

    # @profile
    def _draw_game(self):
        self.game_sprites.update()
        self.game_sprites.draw(self.display)

    def draw(self, bg_color=WHITE):
        self.display.fill(bg_color)
        self._draw_game()

    def resume(self):
        self.isplaying = True
        self.resize_screen(self.w, self.h, True)
