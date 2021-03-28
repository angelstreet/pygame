import pygame as pg
from engine.src.utility import WHITE, BLACK, RED
from engine.src.gamebar import ColorGameBar, ImageGameBar, HeartGameBar
from engine.src.tilemap import TileMap, IsoTileMap
from engine.src.tilemap import Tile
from engine.src.player import Player, IsoPlayer
from engine.src.game_menu import GameMenu
from engine.src.gametext import Text, DynamicText
from engine.src.gamesprite import GameSprite

FPS = 60
FONT_NAME = pg.font.get_default_font()
FONT_SIZE = 14
LAYER_BG = 0
LAYER_GAME = 1
LAYER_UI = 2


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
        self.game_sprites.add(self, layer=5)


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

    def create_player(self, layer, x, y, json, map_x, map_y, tile_w, tile_h, scale=1):
        player = Player(json, map_x, map_y, tile_w, tile_h, scale)
        player.move(x, y)
        self.game_sprites.add(player, layer=layer)
        return player

    def create_isoplayer(self, layer, x, y, json, map_x, map_y, tile_w, tile_h, scale=1):
        isoplayer = IsoPlayer(json, map_x, map_y, tile_w, tile_h, scale)
        isoplayer.move(x, y)
        self.game_sprites.add(isoplayer, layer=layer)
        return isoplayer

    def sortPlayer(self, player):
        x, y = player.get_collision_sprite_center()
        sprites = self.game_sprites.get_sprites_at((x, y))
        for sprite in sprites:
            if isinstance(sprite, Tile):
                if sprite.z<0 :
                    sprites = self.game_sprites.remove_sprites_of_layer(LAYER_GAME)
                    sprites.remove(player)
                    index = sprites.index(sprite)+1
                    sorted_sprites = sprites[:index] + [player] + sprites[index:]
                    print(sprite.i, sprite.j, sprite.z, index)
                    self.game_sprites.add(sorted_sprites, layer=LAYER_GAME)
                    break

# MAP-----------------------------------------------------

    def create_tilemap(self, layer, map_json, map_scale=1, debug=False):
        self.tilemap = TileMap(map_json, map_scale, debug)
        self.game_sprites.add(self.tilemap.get_sprites(), layer=layer)
        return self.tilemap

    def create_isotilemap(self, layer, map_json, map_scale=1, debug=False):
        self.isotilemap = IsoTileMap(map_json, map_scale, debug)
        self.game_sprites.add(self.isotilemap.get_sprites(), layer=layer)
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

    def create_heartgamebar(self,layer, value, total, x, y, json, scale, offset):
        healthbar = HeartGameBar(value, total, x, y, json, scale, offset)
        self.game_sprites.add(healthbar, layer=layer)
        return healthbar
# COLLISION-----------------------------------------------------

    def check_collision(self):
        moving_list = []
        non_moving_list = pg.sprite.Group()
        for sprite in self.game_sprites.sprites():
            if sprite.rigid:
                if sprite.is_moving():
                    moving_list.append(sprite.get_collision_sprite())
                else:
                    non_moving_list.add(sprite.get_collision_sprite())
        for collision_sprite in moving_list:
            # Side collision between 2 losange at z=0
            collision_list = pg.sprite.spritecollide(
                collision_sprite, non_moving_list, False, pg.sprite.collide_mask)
            for sprite in collision_list:
                # Z collision
                if sprite.parent.z <= collision_sprite.parent.z and sprite.parent.z >= collision_sprite.parent.z-collision_sprite.parent.rect.height:
                    collision_sprite.parent.collision_list.append(sprite)
                if sprite.parent.z-sprite.parent.rect.height <= collision_sprite.parent.z and sprite.parent.z >= collision_sprite.parent.z-collision_sprite.parent.rect.height:
                    collision_sprite.parent.collision_list.append(sprite)


# GAME-----------------------------------------------------
    # @profile
    def hide_sprites_for_player(self, player):
        for sprite in self.hided_sprites:
            sprite.remove_blend()
        self.hided_sprites = []
        sprites = self.game_sprites.sprites()
        collision_list = pg.sprite.spritecollide(
            player, sprites, False, pg.sprite.collide_mask)
        for sprite in collision_list:
            if sprite != player and player.zsort() < sprite.zsort():
                sprite.blend((255, 0, 0, 200))
                self.hided_sprites.append(sprite)
        sprites = None


    # @profile
    def _draw_game(self):
        self.game_sprites.update()
        self.game_sprites.draw(self.display)

    def draw(self, color=WHITE):
        self.display.fill(color)
        self._draw_game()
        pg.display.update()

    def resume(self):
        self.isplaying = True
        self.resize_screen(self.w, self.h, True)
