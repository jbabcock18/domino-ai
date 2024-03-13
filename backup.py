import pygame
import sys
from Dominos import Board, BoneYard
from GameDisplay import GameDisplay
from agents.DumbAgent import DumbAgent
from agents.SimpleAgent import SimpleAgent

class Game:
    def __init__(self, players, board, boneyard, display_on=False, verbose=False, wait=0):
        self.boneyard = boneyard
        self.board = board
        self.display_on = display_on
        if display_on:
            self.display = GameDisplay()
            self.display.setup()
        self.players = players
        self.scores = {player.name: 0 for player in players}
        self.wait = wait
        self.verbose = verbose

    def reset(self):
        self.boneyard.reset()
        self.board.reset()
        for player in self.players:
            player.reset(self.board, self.boneyard)
        self.deal()

    def deal(self, num_tiles=5):
        for player in self.players:
            player.draw_n(num_tiles)

    def score(self, idx):
        points = self.board.get_points()
        if points % 5 == 0:
            score = points // 5
            player = self.players[idx]
            self.scores[player.name] += score
            self.log_score(idx, score)
            return score
        return 0
    
    def log_score(self, idx, score):
        if self.verbose:
            print(f"{self.players[idx].name} scored {score} points")

    def play_round(self):
        self.deal()
        

    def play(self):
        self.deal()
        tile_selected, edge_selected = None, None
        round_over = False
        turn = 0
        starting_turn = 0
        skipped = False
        round_num = 0
        while True:
            # Check for round over
            if round_over:
                round_num += 1
                if self.verbose:
                    print("Round", round_num, "scores:", self.scores)
                pygame.time.wait(self.wait * 1000)
                self.reset()
                tile_selected, edge_selected = None, None
                round_over = False
                skipped = False
                starting_turn += 1
                turn = starting_turn
            
                # Check for game over
                for idx, score in enumerate(self.scores):
                    if score >= 61:
                        if self.verbose:
                            print("Game over!")
                            print("{} won".format(self.players[idx].name))
                            print("Final scores:", self.scores)
                        self.scores = [0] * len(self.players)
                        return idx

            # Update turn
            player_index = turn % len(self.players)
            player = self.players[player_index]
            player.turn = True
            for p in self.players:
                if p != player:
                    p.turn = False

            # Draw if no moves
            skip = False
            while len(player.get_moves()) == 0 and len(self.board.edge_tiles) > 0:
                pygame.time.wait(self.wait * 1000)
                can_draw = player.draw()
                if can_draw:
                    if self.verbose:
                        print("{} drew a tile".format(player.name))
                    if self.display_on:
                        self.display.draw_tiles(self.players)
                        pygame.display.flip()

                else:
                    if self.verbose:
                        print("{} cannot draw".format(player.name))
                    turn += 1
                    skip = True
                    break

            if skip and skipped:
                if self.verbose:
                    print("No moves for anyone")
                round_over = True
                continue

            if skip:
                skipped = True
                continue
            else:
                skipped = False

            # Agent move
            if player.is_agent:
                pygame.time.wait(self.wait * 1000)
                tile, edge = player.get_action()
                if tile is None or edge is None:
                    print("player: {}".format(player.name))
                    print("tile: {}, edge: {}".format(tile, edge))
                player.play(tile, edge)
                self.score(player_index)
                turn += 1

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    tile_selected = self.display.handle_tile_click(self.players, x, y)
                    edge_selected = self.display.handle_edge_click(self.board, x, y)
                    if play_button_rect.collidepoint(x, y) and tile_selected:
                        # Handle the logic for playing the selected tile here
                        idx = player.get_index(tile_selected)
                        if edge_selected:
                            edge_idx = self.board.get_index(edge_selected)
                        else:
                            edge_idx = 0
                        if player.play(idx, edge_idx):
                            self.score(player_index)
                            turn += 1
                            tile_selected.selected = False
                            if edge_selected:
                                edge_selected.chosen = False
                            tile_selected = None
                            edge_selected = None

            # Check for game over
            if len(player.hand) == 0:
                if self.verbose:
                    print("{} is out".format(player.name))
                deadwood_points = 0
                for p in self.players:
                    if p != player:
                        deadwood_points += p.deadwood()
                self.scores[player_index] += round(deadwood_points / 5)
                if self.verbose:
                    print("{} scored {} points from deadwood".format(player.name, round(deadwood_points / 5)))
                round_over = True

            if self.display_on:
                self.display.window.fill((100, 100, 100))

                self.display.draw_tiles(self.players)
                self.display.draw_board(self.board)
                self.display.draw_scores(self.scores, self.players)
                play_button_rect = self.display.draw_play_button()

                pygame.display.flip()

board = Board()
boneyard = BoneYard()
p1 = DumbAgent(board=board, boneyard=boneyard)
p2 = SimpleAgent(board=board, boneyard=boneyard)
players = [p1, p2]
game = Game(players, board, boneyard, display_on=False, wait=0)
winner = game.play()
print(winner)