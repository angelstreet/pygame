# AngelStreet @2021
####################################################
import pygame as pg
from engine.src.utility import load_json
from engine.src.tile import Tile


class TileMap():
    def __init__(self, map_json, map_scale, debug=False):
        self.map_json, self.map_scale = map_json, map_scale
        self.debug = debug
        self.map_scale = map_scale
        self.tileset_list_data = {}
        self.tile_list_data = {}
        self.tileset_list = {}
        self.tile_list = {}
        self.tilemap = {}
        self.sprites = []
        self._load_map_json()
        self._create_tileset_list()
        self._create_tile_list()
        self._create_tilemap()

    def _load_map_json(self):
        data = load_json(self.map_json)
        self.tileset_list_data = data['tilemap']['tileset_list']
        self.tile_list_data = data['tilemap']['tile_list']
        self.tilemap_data = data['tilemap']['data']
        self.tilemap_w = data['tilemap']['tilemap_w']
        self.tilemap_h = data['tilemap']['tilemap_h']
        self.tile_w = data['tilemap']['tile_w']*self.map_scale
        self.tile_h = data['tilemap']['tile_h']*self.map_scale

    # 1 - Tileset list
    def _scale_tileset(self, surface):
        rect = surface.get_rect()
        new_w = round(rect.width*self.map_scale)
        new_h = round(rect.height*self.map_scale)
        return pg.transform.scale(surface, (new_w, new_h))

    def _create_tileset_list(self):
        for id, tileset_data in self.tileset_list_data.items():
            path = tileset_data['path']
            colorkey = tileset_data['colorkey']
            self.tileset_list[id] = {}
            self.tileset_list[id]['path'] = path
            self.tileset_list[id]['colorkey'] = colorkey
            if colorkey:
                self.tileset_list[id]['image'] = pg.image.load(path).convert()
                self.tileset_list[id]['image'].set_colorkey(colorkey)
            else:
                self.tileset_list[id]['image'] = pg.image.load(path).convert_alpha()
            self.tileset_list[id]['rect'] = self.tileset_list[id]['image'].get_rect()
            if self.map_scale != 1:
                self.tileset_list[id]['image'] = self._scale_tileset(self.tileset_list[id]['image'])
            self.tileset_list[id]['rect'] = self.tileset_list[id]['image'].get_rect()

    # 2 - Tile list
    def _create_tile_list(self):
        for id, tileset_data in self.tile_list_data.items():
            tile_list_id = str(id)
            self.tile_list[tile_list_id] = {}
            tileset_id = str(tileset_data['tileset'])
            x = round(tileset_data['x'])
            y = round(tileset_data['y'])
            w = round(tileset_data['w']*self.map_scale)
            h = round(tileset_data['h']*self.map_scale)
            self.tile_list[tile_list_id]['tileset'] = tileset_id
            self.tile_list[tile_list_id]['x'], self.tile_list[tile_list_id]['y'] = x, y
            self.tile_list[tile_list_id]['w'], self.tile_list[tile_list_id]['h'] = w, h
            tile_sprite = pg.Surface((w, h), pg.SRCALPHA, 32).convert_alpha()
            tile_sprite.blit(self.tileset_list[tileset_id]['image'], (0, 0), (x, y, w, h))
            self.tile_list[tile_list_id]['image'] = tile_sprite
            self.tile_list[tile_list_id]['rect'] = tile_sprite.get_rect()
    # 3 - Tilemap

    def _create_tilemap(self):
        for z, data in self.tilemap_data.items():
            z *= self.map_scale
            j_list = []
            for j in range(0, self.tilemap_h):
                i_list = []
                for i in range(0, self.tilemap_w):
                    tile = self._create_tile(data, i, j, z)
                    self.move_tile(tile)
                    i_list.append(tile)
                    self.sprites.append(tile)
                j_list.append(i_list)
            self.tilemap[str(z)] = j_list

    # 4 - Tile
    def _create_tile(self, data, i, j, z):
        sprite_list = []
        for layer in data:
            id = str(layer['layer'][j][i])
            if not id == '0':
                sprite = self.tile_list[id]['image']
                sprite_list.append((id, sprite))
        tile = Tile(i, j, z, self.tile_w, self.tile_h, sprite_list)
        return tile

    # ------------------------------------------------------------------
    # Public
    def move_tile(self, tile):
        tile.rect.x = tile.x
        tile.rect.y = tile.y
        print(tile.x,tile.y)

    def get_sprites(self):
        return self.sprites

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

    def zsort(self, tile):
        return 1
