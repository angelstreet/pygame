#AngelStreet @2021
####################################################
import pygame
from src.utility import load_json, cartesian_to_iso
RED = (255, 0, 0)

class Tile(pygame.sprite.Sprite):
    def __init__(self,tilemap, tile_sprite, tile_frame,x,y,z,w,h,isox,isoy,offsetx,offsety,sort):
        pygame.sprite.Sprite.__init__(self)
        self.tilemap=tilemap
        self.tile_sprite=tile_sprite
        self.tile_frame = tile_frame
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.isox = isox
        self.isoy = isoy
        self.offsetx = offsetx
        self.offsety = offsety
        self.sort = sort
        self.init_tile()

    def init_tile(self):
        self.image = pygame.Surface((self.w, self.h),pygame.SRCALPHA, 32).convert_alpha()
        self.image.blit(self.tile_sprite , (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.isox+self.offsetx+self.tilemap.map_w/2+self.tilemap.x
        self.rect.y = self.isoy+self.z+self.offsety+self.tilemap.y

    def isStatic(self):
        return not self.sort

    def zsort(self):
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
        self.sort=True # for debug issues
        self.init_map()
        self.draw_map()

    def load_map_data_from_json(self):
        data = load_json(self.json)
        self.tilesheet_name = data['tilemap']['tilesheet_name']
        self.colorkey = data['tilemap']['colorkey']
        self.tiles_data = data['tilemap']['tiles_data']
        self.map_data = data['tilemap']['map_data']

    def sort_tile(self,tile):
        if not self.sort or tile.isStatic() :
            self.static_tiles.append(tile)
        else:
            self.dynamic_tiles.append(tile)

    def draw_tile(self, x, y, z, tile_frame,sort):
        tile_data = self.tileset[tile_frame-1]
        tile_sprite, w, h, offsetx, offsety = tile_data
        isox, isoy = cartesian_to_iso(x, y, w, h+offsety)
        tile = Tile(self,tile_sprite, tile_frame,x,y,z,w,h,isox,isoy,offsetx,offsety,sort)
        self.sort_tile(tile)

    def zsort(self, tile):
        return tile['z']

    def draw_tiles(self, x, y, tile_list):
        #if x>1 or y >1 : return
        tile_list.sort(key=self.zsort,reverse=True)
        for tile in tile_list:
            tile_frame = tile['tile_frame']
            z = tile['z']*self.scale
            sort = False
            if 'sort' in tile :
                sort = True
            if tile_frame > 0:
                self.draw_tile(x, y, z, tile_frame,sort)

    def init_map(self):
        self.image = pygame.Surface((self.map_w*self.scale, self.map_h*self.scale),pygame.SRCALPHA, 32).convert_alpha()
        self.image = pygame.Surface((self.map_w,self.map_h),pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()
        self.load_map_data_from_json()
        if self.colorkey:
            self.tilesheet_img = pygame.image.load(self.tilesheet_name).convert()
            self.tilesheet_img.set_colorkey(self.colorkey)
        else :
            self.tilesheet_img = pygame.image.load(self.tilesheet_name).convert_alpha()
        rect = self.tilesheet_img.get_rect()
        self.tilesheet_img = pygame.transform.scale(self.tilesheet_img, (round(rect.width*self.scale), round(rect.height*self.scale)))
        self.tileset = []
        self.tiles = []
        for tile_data in self.tiles_data:
            x,y = tile_data['x'], tile_data['y']
            w,h = tile_data['w'], tile_data['h']
            offsetx,offsety = tile_data['offsetx'], tile_data['offsety']
            x,y,w,h,offsetx,offsety = [int(elt*self.scale) for elt in (x,y,w,h,offsetx,offsety)]
            tile_sprite = pygame.Surface((w, h),pygame.SRCALPHA, 32).convert_alpha()
            tile_sprite.blit(self.tilesheet_img, (0, 0), (x, y, w, h))
            self.tileset.append((tile_sprite,w,h,offsetx,offsety))

        for y, row in enumerate(self.map_data):
            for x, tile_list in enumerate(row):
                self.draw_tiles(x,y,tile_list)

    def draw_map(self) :
        self.image.fill(RED)
        for tile in self.static_tiles :
            print(tile.y,tile.offsety,self.scale,tile.isox,tile.isoy)
            x = tile.isox+tile.offsetx+self.map_w/2
            y = tile.isoy+tile.z+120 #100 is security based on average offsety
            self.image.blit(tile.image,(x,y))
        self.rect.x = self.x
        self.rect.y = self.y

    def getBackground(self):
        return self

    def getTiles(self):
        return self.dynamic_tiles
