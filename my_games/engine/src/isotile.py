#AngelStreet @2021
####################################################
import pygame
from src.gamesprite import GameSprite
from src.utility import load_json, cartesian_to_iso
RED = (255, 0, 0)


class Tile(GameSprite):
    def __init__(self, tilemap, tile_sprite, tile_frame, i, j, z, w, h, x, y, offsetx, offsety, sort, rigid):
        GameSprite.__init__(self)
        self.tilemap = tilemap
        self.tile_sprite = tile_sprite
        self.tile_frame = tile_frame
        self.i = i
        self.j = j
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.offsetx = offsetx
        self.offsety = offsety
        self.sort = sort
        self.rigid = rigid
        self.collision_list = []
        self.init_tile()

    def init_tile(self):
        self.create_surface(self.w, self.h)
        self.blit(self.tile_sprite)
        self.move(self.x+self.offsetx, self.y+self.z+self.offsety)
        self.blits()

    def is_static(self):
        return not self.sort

    def zsort(self):
        return int(200+self.i*100+1000*self.j-self.z)

    def get_collision_sprite(self):
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.Surface((self.rect.size), pygame.SRCALPHA, 32).convert_alpha()
        w, h = self.w, self.h
        polygon_b = [(0, h-h/3), (w/2, h-h/3*2), (w, h-h/3), (w/2, h)]
        pygame.draw.polygon(sprite.image, (255, 255, 0), polygon_b)
        sprite.mask = pygame.mask.from_surface(sprite.image)
        sprite.rect = self.image.get_rect()
        sprite.rect.x = self.rect.x
        sprite.rect.y = self.rect.y-self.z+self.offsety
        # self.image.blit(sprite.image,(0,0))
        sprite.parent = self
        return sprite
