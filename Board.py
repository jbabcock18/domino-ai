class Board:
    def __init__(self):
        self.tiles = []
        self.edge_tiles = []

    def add_edge(self, edge_idx, tile):
        valid = True
        if len(self.edge_tiles) == 0:
            self.tiles.append(tile)
        else:
            valid = self.edge_tiles[edge_idx].add_edge(tile)
            if valid:
                self.tiles.append(tile)

        self.edge_tiles = [tile for tile in self.tiles if not tile.is_full()]
        return valid
    
    def is_empty(self):
        return len(self.tiles) == 0
    
    def reset(self):
        self.tiles = []
        self.edge_tiles = []
    
    def first_tile(self):
        return self.tiles[0]

    def show_tiles(self):
        for tile in self.tiles:
            print(tile)

    def show_edges(self):
        for idx, tile in enumerate(self.edge_tiles):
            print(idx, tile)

    def show_details(self):
        for tile in self.tiles:
            tile.show()        

    def get_index(self, tile):
        for idx, t in enumerate(self.edge_tiles):
            if t == tile:
                return idx
        return 0

    def get_points(self):
        points = 0
        for tile in self.edge_tiles:
            # Uncapped double
            if tile.is_double() and (tile.double_b is None or tile.double_a is None):
                points += tile.a * 2
            # Capped double
            elif tile.is_double() and tile.double_b is not None and tile.double_a is not None:
                continue
            # First tile
            elif tile.a_edge is None and tile.b_edge is None:
                points += tile.a + tile.b
            # Regular edge
            elif tile.a_edge is None:
                points += tile.a
            elif tile.b_edge is None:
                points += tile.b
        return points