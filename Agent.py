from Player import DominoPlayer
import random
import copy

class DumbAgent(DominoPlayer):
    def __init__(self, bone_yard, board):
        super().__init__(bone_yard, board)
        self.name = "Dumb Agent"
        self.is_agent = True

    def get_action(self):
        if self.board.is_empty():
            return (0, 0)
        moves = self.get_moves()
        # pick a random move
        if len(moves) > 0:
            return random.choice(moves)


class SimpleAgent(DominoPlayer):
    def __init__(self, bone_yard, board):
        super().__init__(bone_yard, board)
        self.name = "Simple Agent"
        self.is_agent = True

    def get_action(self):
        max_value = 0
        max_idx = None
        # First tile
        if self.board.is_empty():
            for i in range(len(self.hand)):
                tile = self.hand[i]
                score = self.get_score((i, 0))
                if score > max_value:
                    max_value = score
                    max_idx = i
            if max_idx is not None:       
                return (max_idx, 0)
            return (0, 0)
        
        # Can score?
        moves = self.get_moves()
        if len(moves) == 0:
            print("edge tiles:", self.board.edge_tiles)
            print("hand:", self.hand)
        max_score = 0
        best_move = None
        for move in moves:
            score = self.get_score(move)
            if score > max_score:
                max_score = score
                best_move = move

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
    
    def get_score(self, move):
        tile_idx, edge_idx = move
        tile = self.hand[tile_idx]
        board_copy = copy.deepcopy(self.board)
        tile_copy = copy.deepcopy(tile)
        board_copy.add_edge(edge_idx, tile_copy)
        points = board_copy.get_points()
        if points % 5 == 0:
            return points / 5
        return 0

        

        