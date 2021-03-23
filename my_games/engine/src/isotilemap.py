#AngelStreet @2021
####################################################
import pygame
from src.utility import load_json, cartesian_to_iso
RED = (255, 0, 0)

class Tile(pygame.sprite.Sprite):
    def __init__(self,tilemap, tile_sprite, tile_frame,x,y,z,w,h,isox,isoy,offsetx,offsety,sort,rigid):
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
        self.rigid= rigid
        self.collision_list = []
        self.init_tile()

    def init_tile(self):
        self.image = pygame.Surface((self.w, self.h),pygame.SRCALPHA, 32).convert_alpha()
        self.image.blit(self.tile_sprite , (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = self.isox+self.offsetx+self.tilemap.map_w/2+self.tilemap.x
        self.rect.y = self.isoy+self.z+self.offsety+self.tilemap.y

    def is_static(self):
        return not self.sort

    def zsort(self):
        depth = round(self.rect.y+self.rect.h-self.z)
        return depth

    def is_moving(self) :
        return False

    def get_collision_sprite(self) :
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.Surface((self.rect.size),pygame.SRCALPHA, 32).convert_alpha()
        w,h = self.w,self.h
        polygon_b=[(0,h-h/3), (w/2, h-h/3*2), (w, h-h/3),(w/2, h)]
        pygame.draw.polygon(sprite.image,(255,255,0),polygon_b)
        sprite.mask = pygame.mask.from_surface(sprite.image)
        sprite.rect = self.image.get_rect()
        sprite.rect.x=self.rect.x
        sprite.rect.y=self.rect.y-self.z+self.offsety
        #self.image.blit(sprite.image,(0,0))
        sprite.parent = self
        return sprite

    def update(self):
        pass

class IsoTileMap(pygame.sprite.Sprite):
    def __init__(self,x,y,map_w,map_h, json, scale=1, debug = False):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.map_w = map_w
        self.map_h = map_h
        self.json = json
        self.scale = scale
        self.static_tiles = []
        self.dynamic_tiles = []
        self.debug = debug
        self.init_map()
        self.draw_map()

    def load_map_data_from_json(self):
        data = load_json(self.json)
        self.tilesheet_name = data['tilemap']['tilesheet_name']
        self.colorkey = data['tilemap']['colorkey']
        self.tiles_data = data['tilemap']['tiles_data']
        self.map_data = data['tilemap']['map_data']
        self.tile_w = data['tilemap']['tile_w']
        self.tile_h = data['tilemap']['tile_h']

    def sort_tile(self,tile):
        if tile.is_static() :
            self.static_tiles.append(tile)
        else:
            self.dynamic_tiles.append(tile)

    def draw_tile(self, x, y, z, tile_frame,sort,rigid):
        tile_data = self.tileset[tile_frame-1]
        tile_sprite, w, h, offsetx, offsety = tile_data
        isox, isoy = cartesian_to_iso(x, y, w, h+offsety)
        tile = Tile(self,tile_sprite, tile_frame,x,y,z,w,h,isox,isoy,offsetx,offsety,sort,rigid)
        self.sort_tile(tile)

    def zsort(self, tile):
        return tile['z']

    def draw_tiles(self, x, y, tile_list):
        #if self.debug and (x>3 or y >3) : return
        tile_list.sort(key=self.zsort,reverse=True)
        for tile in tile_list:
            tile_frame = tile['tile_frame']
            z = tile['z']*self.scale
            sort,rigid = False,False
            if 'sort' in tile :
                sort = True
            if 'rigid' in tile :
                rigid = True
            self.draw_tile(x, y, z, tile_frame,sort,rigid)

    def init_map(self):
        self.image = pygame.Surface((self.map_w*self.scale, self.map_h*self.scale),pygame.SRCALPHA, 32).convert_alpha()
        self.image = pygame.Surface((self.map_w,self.map_h),pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()
        self.load_map_data_from_json()
        #Draw spritesheet with all tiles
        if self.colorkey:
            self.tilesheet_img = pygame.image.load(self.tilesheet_name).convert()
            self.tilesheet_img.set_colorkey(self.colorkey)
        else :
            self.tilesheet_img = pygame.image.load(self.tilesheet_name).convert_alpha()
        rect = self.tilesheet_img.get_rect()
        self.tilesheet_img = pygame.transform.scale(self.tilesheet_img, (round(rect.width*self.scale), round(rect.height*self.scale)))
        #Draw each tiles on a sprite
        self.tileset = []
        self.tiles = []
        self.tile_w =int(self.tile_w*self.scale)
        self.tile_h = int(self.tile_h*self.scale)
        for tile_data in self.tiles_data:
            x,y = tile_data['x'], tile_data['y']
            offsetx,offsety = tile_data['offsetx'], tile_data['offsety']
            x,y,offsetx,offsety = [int(elt*self.scale) for elt in (x,y,offsetx,offsety)]
            tile_sprite = pygame.Surface((self.tile_w, self.tile_h),pygame.SRCALPHA, 32).convert_alpha()
            tile_sprite.blit(self.tilesheet_img, (0, 0), (x, y, self.tile_w, self.tile_h))
            if self.debug:self.image.blit(tile_sprite,(x,y))
            self.tileset.append((tile_sprite,self.tile_w,self.tile_h,offsetx,offsety))
        #Draw the tilemap
        for y, row in enumerate(self.map_data):
            for x, tile_list in enumerate(row):
                self.draw_tiles(x,y,tile_list)

    def draw_map(self) :
        #self.image.fill(RED)
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
