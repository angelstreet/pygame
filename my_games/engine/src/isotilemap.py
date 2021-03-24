# AngelStreet @2021
####################################################
import pygame
from src.utility import load_json, cartesian_to_iso
from src.isotile import Tile
from src.gamesprite import GameSprite


class IsoTileMap(GameSprite):
    def __init__(self, x, y, map_w, map_h, json, scale=1, debug=False):
        GameSprite.__init__(self)
        self.x = x
        self.y = y
        self.map_w = map_w
        self.map_h = map_h
        self.json = json
        self.scale = scale
        self.static_tiles = []
        self.dynamic_tiles = []
        self.tiles = []
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

    def sort_tile(self, tile):
        if tile.is_static():
            self.static_tiles.append(tile)
        else:
            self.dynamic_tiles.append(tile)

    def draw_tile(self, i, j, z, tile_frame, sort, rigid):
        tile_data = self.tileset[tile_frame-1]
        tile_sprite, w, h, offsetx, offsety = tile_data
        isox, isoy = cartesian_to_iso(i, j, w, h+offsety)
        tile = Tile(self, tile_sprite, tile_frame, i, j, z, w,
                    h, isox, isoy, offsetx, offsety, sort, rigid)
        self.sort_tile(tile)
        return tile

    def zsort(self, tile):
        return tile['z']

    def update(self):
        pass

    def draw_tiles(self, i, j, tile_list):
        # if self.debug and (x>3 or y >3) : return
        tile_list.sort(key=self.zsort, reverse=True)
        tiles = []
        for tile in tile_list:
            tile_frame = tile['tile_frame']
            z = tile['z']*self.scale
            sort, rigid = False, False
            if 'sort' in tile:
                sort = tile['sort']
            if 'rigid' in tile:
                rigid = True
            tile = self.draw_tile(i, j, z, tile_frame, sort, rigid)
            tiles.append(tile)
        return tiles

    def init_map(self):
        self.create_surface(self.map_w, self.map_h)
        self.load_map_data_from_json()
        # Draw spritesheet with all tiles
        if self.colorkey:
            self.tilesheet_img = pygame.image.load(self.tilesheet_name).convert()
            self.tilesheet_img.set_colorkey(self.colorkey)
        else:
            self.tilesheet_img = pygame.image.load(self.tilesheet_name).convert_alpha()
        rect = self.tilesheet_img.get_rect()
        self.tilesheet_img = pygame.transform.scale(
            self.tilesheet_img, (round(rect.width*self.scale), round(rect.height*self.scale)))
        # Draw each tiles on a sprite
        self.tileset = []
        self.tiles = []
        self.tile_w = int(self.tile_w*self.scale)
        self.tile_h = int(self.tile_h*self.scale)
        for tile_data in self.tiles_data:
            x, y = tile_data['x'], tile_data['y']
            offsetx, offsety = tile_data['offsetx'], tile_data['offsety']
            x, y, offsetx, offsety = [int(elt*self.scale) for elt in (x, y, offsetx, offsety)]
            tile_sprite = pygame.Surface((self.tile_w, self.tile_h),
                                         pygame.SRCALPHA, 32).convert_alpha()
            tile_sprite.blit(self.tilesheet_img, (0, 0), (x, y, self.tile_w, self.tile_h))

            if self.debug:
                self.image.blit(tile_sprite, (x+180, y))
            self.tileset.append((tile_sprite, self.tile_w, self.tile_h, offsetx, offsety))
        # Draw the tilemap
        for j, row in enumerate(self.map_data):
            col = []
            for i, tile_list in enumerate(row):
                col.append(self.draw_tiles(i, j, tile_list))
            self.tiles.append(col)

    def draw_map(self):
        for tile in self.static_tiles:
            x = tile.x+tile.offsetx
            y = tile.y+tile.z+tile.offsety  # 100 is security based on average offsety
            self.blit(tile.image, (x+self.map_w/2,y+50), False)
        self.blits()
        self.rect.x = self.x-self.map_w/2
        self.rect.y = self.y-50

    def getBackground(self):
        return self

    def getTiles(self):
        return self.dynamic_tiles

    def check_path(self, paths, tree, src_i, src_j, dst_i, dst_j):
        paths.append((src_i, src_j))
        r_tile, l_tile, u_tile, d_tile, move_h, move_v = None, None, None, None, None, None
        if src_i+1 < len(self.tiles):
            r_tile = self.tiles[src_j][src_i+1]
        if src_i-1 >= 0:
            l_tile = self.tiles[src_j][src_i-1]
        if src_j+1 < len(self.tiles):
            u_tile = self.tiles[src_j+1][src_i]
        if src_j-1 >= 0:
            d_tile = self.tiles[src_j-1][src_i]
        # Reach the end
        if src_i == dst_i and src_j == dst_j:
            # print("------------------------Found Path", paths)
            tree.append(paths)
            return paths, tree
        # Check Right or Left or Both
        if r_tile and src_i < dst_i and not (r_tile == [] or r_tile[0].rigid) and not (src_i+1, src_j) in paths:
            # print("right", src_i, src_j, dst_i, dst_j, paths)
            paths, tree = self.check_path(paths, tree, src_i+1, src_j, dst_i, dst_j)
            index = paths.index((src_i, src_j))
            paths = paths[:index+1]
            move_h = True
        elif l_tile and src_i > dst_i and not (l_tile == [] or l_tile[0].rigid) and not (src_i-1, src_j) in paths:
            # print("left", src_i, src_j, dst_i, dst_j, paths)
            paths, tree = self.check_path(paths, tree, src_i-1, src_j, dst_i, dst_j)
            index = paths.index((src_i, src_j))
            paths = paths[:index+1]
            move_h = True
        # Check Up or Down or Both
        if u_tile and src_j < dst_j and not (u_tile == [] or u_tile[0].rigid) and not (src_i, src_j+1) in paths:
            #  print("up", src_i, src_j, dst_i, dst_j, paths)
            paths, tree = self.check_path(paths, tree, src_i, src_j+1, dst_i, dst_j)
            index = paths.index((src_i, src_j))
            paths = paths[:index+1]
            move_v = True
        elif d_tile and src_j > dst_j and not (d_tile == [] or d_tile[0].rigid) and not (src_i, src_j-1) in paths:
            # print("down", src_i, src_j, dst_i, dst_j, paths)
            paths, tree = self.check_path(paths, tree, src_i, src_j-1, dst_i, dst_j)
            index = paths.index((src_i, src_j))
            paths = paths[:index+1]
            move_v = True
        # If could not move
        if src_i == dst_i and not move_v and not move_h:
            if r_tile and not (r_tile == [] or r_tile[0].rigid) and not (src_i+1, src_j) in paths:
                # print("right2", src_i, src_j, dst_i, dst_j, paths)
                paths, tree = self.check_path(paths, tree, src_i+1, src_j, dst_i, dst_j)
                index = paths.index((src_i, src_j))
                paths = paths[:index+1]
            if l_tile and not (l_tile == [] or l_tile[0].rigid) and not (src_i-1, src_j) in paths:
                # print("left2", src_i, src_j, dst_i, dst_j, paths)
                paths, tree = self.check_path(paths, tree, src_i-1, src_j, dst_i, dst_j)
                index = paths.index((src_i, src_j))
                paths = paths[:index+1]
        elif src_j == dst_j and not move_h and not move_v:
            if u_tile and not (u_tile == [] or u_tile[0].rigid) and not (src_i, src_j+1) in paths:
                # print("up2", src_i, src_j, dst_i, dst_j, paths)
                paths, tree = self.check_path(paths, tree, src_i, src_j+1, dst_i, dst_j)
                index = paths.index((src_i, src_j))
                paths = paths[:index+1]
            if d_tile and not (d_tile == [] or d_tile[0].rigid) and not (src_i, src_j-1) in paths:
                # print("down2", src_i, src_j, dst_i, dst_j, paths)
                paths, tree = self.check_path(paths, tree, src_i, src_j-1, dst_i, dst_j)
                index = paths.index((src_i, src_j))
                paths = paths[:index+1]

        return paths, tree

    def get_path(self, src, dst):
        tile_list = []
        # print("Source", src.i, src.j, "Destination", dst.i, dst.j)
        _, tree = self.check_path([], [], src.i, src.j, dst.i, dst.j)
        print("Paths found :", len(tree), "---------------------")
        if tree == []:
            return tree
        best_path_score, best_paths = None, None
        for path in tree:
            if not best_paths or len(path) < best_path_score:
                best_paths = [path]
                best_path_score = len(path)
            elif len(path) == best_path_score:
                best_paths.append(path)
        print("Best paths found :", len(best_paths), " with score :",
              str(best_path_score), " ---------------------")
        for path in best_paths:
            col = []
            for t in path:
                tile = self.tiles[t[1]][t[0]][0]
                col.append(tile)
            tile_list.append(col)
        return tile_list, best_path_score
