#AngelStreet @2021
####################################################
import sys,os,pygame
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utility import load_json
WHITE = (255, 255, 255)
RED = (255, 0, 0)
MAPOFFSETX, MAPOFFSETY = 500, 100

# FUNCTIONS----------------------
def get_tilemap(tilemap_json_file):
    data = load_json('tilemap.json')
    tilesheet_name = data['tilemap']['tilesheet_name']
    colorkey = data['tilemap']['colorkey']
    tiles_data = data['tilemap']['tiles_data']
    map_data = data['tilemap']['map_data']
    #print(tilesheet_name, colorkey, tiles_data, map_data)
    return tilesheet_name, colorkey, tiles_data, map_data

def get_sprite(sprite_sheet, x, y, w, h):
    sprite = pygame.Surface((w, h))
    sprite.set_colorkey((0, 255, 0))
    sprite.blit(sprite_sheet, (0, 0), (x, y, w, h))
    return sprite


def cartesian_to_iso(x, y, w, h):
    iso_x = round((x - y) * w/2)
    iso_y = round((x + y) * h/2)
    return iso_x, iso_y


def draw_map(screen, display):
    display.fill(WHITE)
    tilesheet_name, colorkey, tiles_data, map_data = get_tilemap('tilemap.json')
    tilesheet_img = pygame.image.load(tilesheet_name).convert()
    tiles = []
    tile_sprite = get_sprite(tilesheet_img, 0, 0, 160, 120)
    #display.blit(tile_sprite, (500,200))
    for tile_data in tiles_data:
        w,h = tile_data['w'], tile_data['h']
        x,y = tile_data['x'], tile_data['y']
        offsetx,offsety = tile_data['offsetx'], tile_data['offsety']
        print(x,y,w,h,offsetx,offsety)
        tile_sprite = get_sprite(tilesheet_img, x, y, w, h)
        tiles.append((tile_sprite,w,h,offsetx,offsety))
        #display.blit(tile_sprite, (500,x))
    #return
    for y, row in enumerate(map_data):
        for x, tile_id in enumerate(row):
            tile=tiles[tile_id]
            tile_sprite,w,h,offsetx,offsety = tile
            isox, isoy = cartesian_to_iso(x, y, w-offsetx, h-offsety)
            display.blit(tile_sprite, (MAPOFFSETX+isox, MAPOFFSETY+isoy))
