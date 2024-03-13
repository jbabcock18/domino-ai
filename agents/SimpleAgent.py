from Player import DominoPlayer
import copy

class SimpleAgent(DominoPlayer):
    def __init__(self, name="Simple Agent"):
        super().__init__()
        self.name = name
        self.is_agent = True
        

    def get_action(self, board):
        max_value = 0
        max_idx = None
        # First tile
        if board.is_empty():
            for i in range(len(self.hand)):
                tile = self.hand[i]
                score = self.get_score(board, (i, 0))
                if score > max_value:
                    max_value = score
                    max_idx = i
            if max_idx is not None:       
                return (max_idx, 0)
            return (0, 0)
        
        # Can score?
        moves = self.get_moves(board)
        if len(moves) == 0:
            return None
        max_score = 0
        best_move = None
        for move in moves:
            score = self.get_score(board, move)
            if score > max_score:
                max_score = score
                best_move = move
                
        # Can't score
        if best_move is None:
            # Choose highest tile in valid moves
            max_value = 0
            best_move = moves[0]
            for move in moves:
                tile_idx, edge_idx = move
                tile = self.hand[tile_idx]
                value = tile.value()
                if value > max_value:
                    max_value = value
                    best_move = move

        return best_move
    
    def play(self, board, move):
        tile_idx, edge_idx = move
        tile = self.hand[tile_idx]
        valid = board.add_edge(edge_idx, tile)
        if valid:
            self.hand.pop(tile_idx)
        return valid
    
    def get_score(self, board, move):
        tile_idx, edge_idx = move
        tile = self.hand[tile_idx]
        board_copy = copy.deepcopy(board)
        tile_copy = copy.deepcopy(tile)
        board_copy.add_edge(edge_idx, tile_copy)
        points = board_copy.get_points()
        if points % 5 == 0:
            return points / 5
        return 0

        

        