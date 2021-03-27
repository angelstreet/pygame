# AngelStreet @2021
####################################################
from engine.src.utility import cartesian_to_iso
from engine.src.tilemap import TileMap


class IsoTileMap(TileMap):
    def __init__(self,map_json, map_scale=1, debug=False):
        TileMap.__init__(self, map_json, map_scale, debug=False)

    # ------------------------------------------------------------------
    # Public
    def move_tile(self,tile) :
        tile.rect.x,tile.rect.y = cartesian_to_iso(tile.x,tile.y,self.tile_w,self.tile_h)
