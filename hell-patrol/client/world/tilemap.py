from .terrain_generator import generate_base_map
from .bigtile_generator import generate_big_tiles
from .structure_generator import generate_structures
from .renderer import draw_tilemap

class TileMap:
    def __init__(self, tiles, tile_ids, weights):
        self.tiles = tiles
        self.map, self.row_offset = generate_base_map(tile_ids, weights)
        self.big_tiles = generate_big_tiles()
        self.gates = generate_structures()

    def draw(self, screen, camera):
        draw_tilemap(
            screen,
            camera,
            self.tiles,
            self.map,
            self.row_offset,
            self.big_tiles,
            self.gates
        )
