from Domino import Tile

class DominoPlayer:
    def __init__(self, bone_yard, board):
        self.hand = []
        self.bone_yard = bone_yard
        self.board = board
        self.name = "Jack"
        self.is_agent = False
        self.turn = False

    def draw(self):
        tile = self.bone_yard.draw()
        if tile is None:
            return False
        self.hand.append(tile)
        return True

    def show(self):
        for idx, tile in enumerate(self.hand):
            print(idx, tile)

    def get_index(self, tile):
        for idx, t in enumerate(self.hand):
            if t == tile:
                return idx
        return 0
    
    def deadwood(self):
        deadwood = 0
        for tile in self.hand:
            deadwood += tile.a + tile.b
        return deadwood
    
    def play(self, tile_idx, edge_idx):
        tile = self.hand[tile_idx]
        valid = self.board.add_edge(edge_idx, tile)
        if valid:
            self.hand.pop(tile_idx)
        return valid
    
    def get_moves(self):
        moves = []
        for idx, tile in enumerate(self.hand):
            for edge_idx, edge in enumerate(self.board.edge_tiles):
                if tile is None or edge is None:
                    return []
                elif edge.can_play(tile):
                    moves.append((idx, edge_idx))
        return moves
        
    def get_remaining_tiles(self):
        remaining = []
        for i in range(7):
            for j in range(i, 7):
                remaining.append(Tile(i, j))
        for tile in self.hand:
            remaining.remove(tile)
        for tile in self.board.tiles:
            remaining.remove(tile)
        return remaining
        
