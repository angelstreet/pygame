#AngelStreet @2021
####################################################
import pygame
from src.utility import load_json, cartesian_to_iso
RED = (255, 0, 0)

class Tile(pygame.sprite.Sprite):
    def __init__(self,tile_sprite, tile_frame,map_w, x,y,z,w,h,isox,isoy,offsetx,offsety,scale,sort):
        pygame.sprite.Sprite.__init__(self)
        self.tile_sprite=tile_sprite
        self.tile_frame = tile_frame
        self.map_w = map_w
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.isox = isox
        self.isoy = isoy
        self.offsetx = offsetx
        self.offsety = offsety
        self.scale = scale
        self.sort = sort
        self.init_tile()

    def init_tile(self):
        self.image = pygame.transform.scale(self.tile_sprite, (round(self.w*self.scale), round(self.h*self.scale)))
        self.rect = self.image.get_rect()
        self.rect.x=self.isox+self.map_w/2
        self.rect.y=self.isoy+self.z

    def isStatic(self):
        return not self.sort

    def zsort(self):
        if self.z>0 :
            depth = round(self.rect.y+self.rect.h-10*self.z)
        else :
            depth = round(self.rect.y+self.rect.h-self.z)
        return depth

    def update(self):
        pass

    def __str__(self):
        return "Tile - tile_frame:%s, x:%s, y:%s, z:%s, w:%s, h:%s, isox:%s, isoy:%s, offsetx:%s, offsety:%s, scale:%s" % (self.tile_frame,self.x,self.y,self.z,self.w,self.h,self.isox,self.isoy,self.offsetx,self.offsety,self.scale)

class IsoTileMap(pygame.sprite.Sprite):
    def __init__(self,x,y,map_w,map_h, json, scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.map_w = map_w
        self.map_h = map_h
        self.json = json
        self.scale = scale
        self.static_tiles = []
        self.dynamic_tiles = []
        self.init_map()
        self.draw_map()

    def load_map_data_from_json(self):
        data = load_json(self.json)
        self.tilesheet_name = data['tilemap']['tilesheet_name']
        self.colorkey = data['tilemap']['colorkey']
        self.tiles_data = data['tilemap']['tiles_data']
        self.map_data = data['tilemap']['map_data']

    def sort_tile(self,tile):
        if tile.isStatic() :
            self.static_tiles.append(tile)
        else:
            self.dynamic_tiles.append(tile)

    def draw_tile(self, x, y, z, tile_frame,sort):
        tile_data = self.tileset[tile_frame-1]
        tile_sprite, w, h, offsetx, offsety = tile_data
        isox, isoy = cartesian_to_iso(x, y, w*self.scale-offsetx*self.scale, h*self.scale-offsety*self.scale)
        tile = Tile(tile_sprite, tile_frame,self.map_w,x,y,z,w,h,isox+self.x,isoy+self.y,offsetx,offsety,self.scale,sort)
        self.sort_tile(tile)


    def draw_tiles(self, x, y, tile_list):
        for tile in tile_list:
            tile_frame = tile['tile_frame']
            z = tile['z']
            sort = False
            if 'sort' in tile :
                sort = True
            if tile_frame > 0:
                self.draw_tile(x, y, z, tile_frame,sort)

    def init_map(self):
        self.image = pygame.Surface((self.map_w*self.scale, self.map_h*self.scale),pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()
        self.load_map_data_from_json()
        if self.colorkey:
            print("test")
            self.tilesheet_img = pygame.image.load(self.tilesheet_name).convert()
            self.tilesheet_img.set_colorkey(self.colorkey)
        else :
            self.tilesheet_img = pygame.image.load(self.tilesheet_name).convert_alpha()

        self.tileset = []
        self.tiles = []
        for tile_data in self.tiles_data:
            x,y = tile_data['x'], tile_data['y']
            w,h = tile_data['w'], tile_data['h']
            offsetx,offsety = tile_data['offsetx'], tile_data['offsety']
            tile_sprite = pygame.Surface((w, h),pygame.SRCALPHA, 32).convert_alpha()
            tile_sprite.blit(self.tilesheet_img, (0, 0), (x, y, w, h))
            self.tileset.append((tile_sprite,w,h,offsetx,offsety))
        for y, row in enumerate(self.map_data):
            for x, tile_list in enumerate(row):
                self.draw_tiles(x,y,tile_list)

    def draw_map(self) :
        for tile in self.static_tiles :
            self.image.blit(tile.image,(tile.isox+self.map_w/2,tile.isoy))

    def getBackground(self):
        return self

    def getTiles(self):
        return self.dynamic_tiles
