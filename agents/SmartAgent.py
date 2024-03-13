from Player import DominoPlayer
import copy

class SmartAgent(DominoPlayer):
    def __init__(self, name="Smart Agent"):
        super().__init__()
        self.name = name
        self.is_agent = True



class GameState:
    def __init__(self, game):
        self.game = game
        scores = [self.scores[player.name] for player in self.players]
        self.score = scores[0] - scores[1]

    def get_possible_moves(self):
        moves = self.game.current_player.get_moves(self.game.board)
        return moves
    
    def get_next_state(self, move):
        new_game = copy.deepcopy(self.game)
        new_game.handle_agent_play(move)
        return GameState(new_game)
    
    def is_terminal(self):
        return self.game.round_over()
    
    