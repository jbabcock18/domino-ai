from Dominos import Tile

class DominoPlayer:
    def __init__(self, name="Jack"):
        self.hand = []
        self.name = name
        self.is_agent = False

    def draw(self, boneyard):
        tile = boneyard.draw()
        if tile is None:
            return False
        self.hand.append(tile)
        return True
    
    def draw_n(self, boneyard, n):
        for i in range(n):
            self.draw(boneyard)

    def show(self):
        for idx, tile in enumerate(self.hand):
            print(idx, tile)

    def get_tile_index(self, tile):
        for tile_idx, t in enumerate(self.hand):
            if t == tile:
                return tile_idx
        return 0
    
    def deadwood(self):
        deadwood = 0
        for tile in self.hand:
            deadwood += tile.a + tile.b
        return deadwood
    
    def play(self, board, tile, edge):
        tile_idx = self.get_tile_index(tile)
        if edge:
            edge_idx = board.get_index(edge)
        else:
            edge_idx = 0

        tile = self.hand[tile_idx]
        valid = board.add_edge(edge_idx, tile)
        if valid:
            self.hand.pop(tile_idx)
        return valid
    
    def get_moves(self, board):
        if board.is_empty():
            return [(i, 0) for i in range(len(self.hand))]
        moves = []
        for idx, tile in enumerate(self.hand):
            for edge_idx, edge in enumerate(board.edge_tiles):
                if tile is None or edge is None:
                    return []
                elif edge.can_play(tile):
                    moves.append((idx, edge_idx))
        return moves
        
    def get_remaining_tiles(self, board):
        remaining = []
        for i in range(7):
            for j in range(i, 7):
                remaining.append(Tile(i, j))
        for tile in self.hand:
            remaining.remove(tile)
        for tile in board.tiles:
            remaining.remove(tile)
        return remaining
    
    def reset(self):
        self.hand = []
        
