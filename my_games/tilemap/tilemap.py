#AngelStreet @2021
####################################################
import sys,os,pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utility import load_json,get_sprite,cartesian_to_iso
RED = (255, 0, 0)
MAP_WIDTH, MAP_HEIGHT = 1200,800
MAPOFFSETX, MAPOFFSETY = 500, 100


class Map(pygame.sprite.Sprite):
    def __init__(self, json,scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.json = json
        self.scale = scale
        self.init_map()

    def load_map_data_from_json(self):
        data = load_json(self.json)
        self.tilesheet_name = data['tilemap']['tilesheet_name']
        self.colorkey = data['tilemap']['colorkey']
        self.tiles_data = data['tilemap']['tiles_data']
        self.map_data = data['tilemap']['map_data']

    def init_map(self):
        self.image = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0,0,0))
        self.load_map_data_from_json()
        self.tilesheet_img = pygame.image.load(self.tilesheet_name).convert()
        tiles = []
        for tile_data in self.tiles_data:
            x,y = tile_data['x'], tile_data['y']
            w,h = tile_data['w'], tile_data['h']
            offsetx,offsety = tile_data['offsetx'], tile_data['offsety']
            tile_sprite = get_sprite(self.tilesheet_img, x, y, w, h,self.colorkey)
            tiles.append((tile_sprite,w,h,offsetx,offsety))
        for y, row in enumerate(self.map_data):
            for x, tile_id in enumerate(row):
                tile=tiles[tile_id]
                tile_sprite,w,h,offsetx,offsety = tile
                isox, isoy = cartesian_to_iso(x, y, w-offsetx, h-offsety)
                self.image.blit(tile_sprite, (MAPOFFSETX+isox, MAPOFFSETY+isoy))
