#AngelStreet @2021
####################################################
import pygame, random
from utility import load_json, get_sprite, cartesian_to_iso, move_sprite
RED = (255, 0, 0)
MAP_WIDTH, MAP_HEIGHT = 1000, 600
MAP_X= 80
MAP_Y = 80

class Tile(pygame.sprite.Sprite):
    def __init__(self,tile_sprite, tile_frame,x,y,z,w,h,isox,isoy,offsetx,offsety,colorkey,scale,sort):
        pygame.sprite.Sprite.__init__(self)
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
        self.colorkey = colorkey
        self.scale = scale
        self.sort = sort
        self.init_tile()

    def init_tile(self):
        self.image = pygame.transform.scale(self.tile_sprite, (round(self.w*self.scale), round(self.h*self.scale)))
        self.rect = self.image.get_rect()
        self.rect.x=self.isox+MAP_WIDTH/2+MAP_X
        self.rect.y=self.isoy+MAP_Y+self.z

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
        return "Tile - tile_frame:%s, x:%s, y:%s, z:%s, w:%s, h:%s, isox:%s, isoy:%s, offsetx:%s, offsety:%s, colorkey:%s, scale:%s" % (self.tile_frame,self.x,self.y,self.z,self.w,self.h,self.isox,self.isoy,self.offsetx,self.offsety,self.colorkey,self.scale)

class Map(pygame.sprite.Sprite):
    def __init__(self, json, scale=1):
        pygame.sprite.Sprite.__init__(self)
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
        tile = Tile(tile_sprite, tile_frame,x,y,z,w,h,isox,isoy,offsetx,offsety,self.colorkey,self.scale,sort)
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
        self.image = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
        self.rect = self.image.get_rect()
        self.load_map_data_from_json()
        self.tilesheet_img = pygame.image.load(self.tilesheet_name).convert()
        self.image.set_colorkey((0,0,0))
        self.tileset = []
        self.tiles = []
        for tile_data in self.tiles_data:
            x,y = tile_data['x'], tile_data['y']
            w,h = tile_data['w'], tile_data['h']
            offsetx,offsety = tile_data['offsetx'], tile_data['offsety']
            tile_sprite = get_sprite(self.tilesheet_img, x, y, w, h,self.colorkey)
            self.tileset.append((tile_sprite,w,h,offsetx,offsety))
        for y in range(0,30):
            for x in range(0,30):
                tile_frame = random.choice([1,1,1,1,1,2,2,2,2,3,5,5])
                tile_list = [{"tile_frame":tile_frame,"z":0,"sort":False}]
                self.draw_tiles(x,y,tile_list)

    def draw_map(self) :
        self.rect.x = MAP_X
        self.rect.y = MAP_Y
        for tile in self.static_tiles :
            self.image.blit(tile.image,(tile.isox+MAP_WIDTH/2,tile.isoy))

    def move(self, x, y):
        move_sprite(self, x, y)

    def zsort(self):
        return 1
