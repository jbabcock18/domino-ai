import pygame
import sys
from Domino import *
from GameDisplay import *
from Agent import *
from Board import *
from Player import *

class Game:
    def __init__(self, num_players=2, verbose=False, wait=0):
        self.boneyard = BoneYard()
        self.boneyard.shuffle()
        self.board = Board()
        self.display = GameDisplay()
        self.players = []
        self.scores = [0] * num_players
        self.wait = wait
        self.verbose = verbose
        # self.players.append(DominoPlayer(self.boneyard, self.board))
        rando = DumbAgent(self.boneyard, self.board)
        simp = SimpleAgent(self.boneyard, self.board)
        self.players.append(rando)
        self.players.append(simp)

    def reset(self):
        self.boneyard = BoneYard()
        self.boneyard.shuffle()
        self.board.reset()
        for player in self.players:
            player.hand = []
            player.board = self.board
            player.bone_yard = self.boneyard
        self.deal()

    def deal(self):
        for player in self.players:
            for i in range(5):
                player.draw()

    def score(self, idx):
        points = self.board.get_points()
        if points % 5 == 0:
            score = points / 5
            self.scores[idx] += score
            player = self.players[idx]
            if self.verbose:
                print("{} scored {} points".format(player.name, int(score)))
            return score
        return 0

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
                    if score > 61:
                        print("Game over!")
                        print("{} won".format(self.players[idx].name))
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
                    tile_selected = self.display.handle_click(self.players, x, y)
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


            self.display.window.fill((100, 100, 100))

            self.display.draw_tiles(self.players)
            self.display.draw_board(self.board)
            self.display.draw_scores(self.scores, self.players)
            play_button_rect = self.display.draw_play_button()

            pygame.display.flip()


game = Game(2)
winner = game.play()
print("Winner:", winner)