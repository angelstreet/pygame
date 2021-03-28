# AngelStreet @2021
####################################################
import pygame as pg
RED = (255, 0, 0)


class Tile(pg.sprite.Sprite):
    def __init__(self, i, j, z, tile_w, tile_h, tile_list):
        pg.sprite.Sprite.__init__(self)
        self.i, self.j, self.z = i, j, z
        self.tile_w, self.tile_h = tile_w, tile_h
        self.tile_list = tile_list
        self._init_tile()

    def _init_tile(self):
        self.image = pg.Surface((self.tile_w, self.tile_h), pg.SRCALPHA, 32).convert_alpha()
        for _, sprite in self.tile_list:
            self.image.blit(sprite, (0, 0))
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.x = self.i*self.tile_w
        self.y = self.j*self.tile_h

    # ------------------------------------------------------------------
    # Public
    def get_collision_sprite(self):
        sprite = pg.sprite.Sprite()
        sprite.image = pg.Surface((self.rect.size), pg.SRCALPHA, 32).convert_alpha()
        w, h = self.rect.width, self.rect.h
        polygon_b = [(0, h-h/3), (w/2, h-h/3*2), (w, h-h/3), (w/2, h)]
        pg.draw.polygon(sprite.image, (255, 255, 0), polygon_b)
        sprite.mask = pg.mask.from_surface(sprite.image)
        sprite.rect = self.image.get_rect()
        sprite.rect.x = self.rect.x
        sprite.rect.y = self.rect.y
        sprite.parent = self
        return sprite

    def zsort(self):
        depth = int(200+self.i*100+1000*self.j-self.z)
        return depth
