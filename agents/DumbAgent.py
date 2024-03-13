from Player import DominoPlayer
import random

class DumbAgent(DominoPlayer):
    def __init__(self, name="Dumb Agent"):
        super().__init__()
        self.name = name
        self.is_agent = True

    def get_action(self, board):
        if board.is_empty():
            return (0, 0)
        moves = self.get_moves(board)
        # pick a random move
        if len(moves) > 0:
            return random.choice(moves)


    def play(self, board, move):
        tile_idx, edge_idx = move
        tile = self.hand[tile_idx]
        valid = board.add_edge(edge_idx, tile)
        if valid:
            self.hand.pop(tile_idx)
        return valid