import pygame as pg
from engine.src.utility import WHITE, BLACK, RED, GREEN, move_sprite, load_image
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
    def move_sprite(self, sprite,  x, y, replace=False):
        move_sprite(sprite, x, y, replace)

    def resize_screen(self, w, h, resizable=False):
        if resizable:
            pg.display.set_mode((w, h), pg.RESIZABLE)
        else:
            pg.display.set_mode((w, h))

    def add_text(self, layer, x, y, text, font_name, size, color, bg_color, sprite=None):
        text = Text(x, y, text, font_name, size, color, bg_color,  sprite)
        self.game_sprites.add(text, layer=layer)
        return text

    def add_dynamic_text(self, layer, x, y, text, font_name, size, color, bg_color, sprite=None):
        text = DynamicText(x, y, text, font_name, size, color, bg_color,  sprite)
        self.game_sprites.add(text, layer=layer)
        return text

    def add_button(self, layer, x, y, w, h,  text, font_name, font_size, font_color, bg_color):
        btn = Button(w, h, text, font_name, font_size, font_color, bg_color)
        move_sprite(btn, x, y)
        self.game_sprites.add(btn, layer=layer)
        return btn

    def add_image(self, layer, x, y, img_path, alpha=None, colorkey=None, scale=1, sprite=None):
        img = load_image(img_path, alpha, colorkey, scale)
        move_sprite(img, x, y)
        self.game_sprites.add(img, layer=layer)
        img.w, img.h = img.rect.width, img.rect.height
        return img

    def add_sprite(self, layer, x, y, sprite):
        move_sprite(sprite, x, y)
        self.game_sprites.add(sprite, layer=layer)
        sprite.w, sprite.h = sprite.rect.width, sprite.rect.height
        return sprite

    def add_parallax_bg(self, layer, x, y, path, colorkey=None, flip=False, image=None):
        bg_1 = pg.sprite.Sprite()
        if image:
            img_1 = image
        else:
            img_1 = load_image(path).image
        rect_1 = img_1.get_rect()
        iteration = int(self.w/rect_1.width)
        bg_1.image = pg.Surface((rect_1.width*(iteration+1), rect_1.height))
        bg_1.image.blit(img_1, (0, 0))
        for i in range(1, iteration+1):
            img_2 = pg.transform.flip(img_1, flip, False)
            flip = not flip
            bg_1.image.blit(img_2, (i*rect_1.width, 0), (0, 0, rect_1.width, rect_1.height))
        bg_1.rect = bg_1.image.get_rect()
        bg_1.w, bg_1.h = bg_1.rect.width, bg_1.rect.height
        if colorkey:
            bg_1.image.set_colorkey(colorkey)
        move_sprite(bg_1, x, y)
        self.game_sprites.add(bg_1, layer=layer)
        return bg_1

    def add_tiles_bg(self, layer, x, y, tile_w, tile_h, tiles_path, tile_map, colorkey=None):
        t_1 = pg.sprite.Sprite()
        w = tile_w*len(tile_map[0][0])
        h = tile_h*len(tile_map[0])
        t_1.image = pg.Surface((w, h), pg.SRCALPHA, 32).convert_alpha()
        if colorkey:
            t_1.image.set_colorkey(colorkey)
        tile_list = []
        posx, posy = 0, 0
        for path in tiles_path:
            img = load_image(path, True, colorkey)
            tile_list.append(img)
        for l in tile_map:
            for row in l:
                for tile_id in row:
                    if tile_id > 0:
                        tile = tile_list[tile_id-1]
                        if colorkey:
                            tile.image.set_colorkey(colorkey)
                        t_1.image.blit(tile.image, (posx, posy), (0, 0, tile.w, tile.h))
                        posx += tile.w
                posy += tile.h
                posx = 0
            posy = 0
        return self.add_parallax_bg(layer, x, y, None, None, False, t_1.image)
# MENU-----------------------------------------------------

    def hide_game_menu(self):
        self.game_sprites.remove(self.game_menu)

    def show_game_menu(self, layer):
        self.game_sprites.add(self.game_menu, layer=layer)

# ISOPLAYER-----------------------------------------------------
    def add_h_player(self, layer, x, y, json, scale=1, force_right=False):
        player = HorizontalPlayer(layer+2, json, scale, force_right)
        player.move(x, y)
        self.game_sprites.add(player)
        return player

    def add_v_player(self, layer, x, y, json, scale=1, force_up=False):
        player = VerticalPlayer(layer+2, json, scale, force_up)
        player.move(x, y)
        self.game_sprites.add(player)
        return player

    def add_4D_player(self, layer, x, y, json, scale=1):
        player = FourDirPlayer(layer+2, json, scale)
        player.move(x, y)
        self.game_sprites.add(player)
        return player

    def add_4D_iso_player(self, layer, x, y, json, scale=1):
        player = FourDirIsoPlayer(layer+2, json, scale)
        player.move(x, y)
        self.game_sprites.add(player)
        return player

    def add_8D_player(self, layer, x, y, json, scale=1, force_up=False):
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

# MAP-----------------------------------------------------

    def add_tilemap(self, layer, map_json, map_scale=1, debug=False):
        self.tilemap = TileMap(layer, map_json, map_scale, debug)
        self.game_sprites.add(self.tilemap.get_sprites())
        return self.tilemap

    def add_isotilemap(self, layer, map_json, map_scale=1, debug=False):
        self.isotilemap = IsoTileMap(layer, map_json, map_scale, debug)
        self.game_sprites.add(self.isotilemap.get_sprites())
        return self.isotilemap
# HEALTHBAR-----------------------------------------------------

    def add_colorgamebar(self, layer, x, y, value, total,  w, h):
        colorgamebar = ColorGameBar(x, y, value, total,  w, h)
        self.game_sprites.add(colorgamebar, layer=layer)
        return colorgamebar

    def add_imagegamebar(self, layer, x, y, value, total, bg_img, fill_img, fill_offset, scale, alpha=True, keycolor=False):
        imagegamebar = ImageGameBar(x, y, value, total, bg_img, fill_img,
                                    fill_offset, scale, alpha, keycolor)
        self.game_sprites.add(imagegamebar, layer=layer)
        return imagegamebar

    def add_heartgamebar(self, layer, x, y, value, total,  json, scale, offset):
        healthbar = HeartGameBar(x, y, value, total,  json, scale, offset)
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
