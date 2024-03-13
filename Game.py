import pygame
import sys
from Dominos import Board, BoneYard
from GameDisplay import GameDisplay
from agents.DumbAgent import DumbAgent
from agents.SimpleAgent import SimpleAgent

class Game:
    def __init__(self, players, board, boneyard, display_on=False):
        self.boneyard = boneyard
        self.board = board
        self.display_on = display_on
        if display_on:
            self.display = GameDisplay()
            self.display.setup()
        self.players = players
        self.starting_turn = 0
        self.current_player = players[self.starting_turn]
        self.scores = {player.name: 0 for player in players}

    def reset(self):
        self.boneyard.reset()
        self.board.reset()
        self.starting_turn += 1
        self.current_player = self.players[self.starting_turn % len(self.players)]
        for player in self.players:
            player.reset()
        self.deal()

    def deal(self, num_tiles=5):
        for player in self.players:
            player.draw_n(self.boneyard, num_tiles)
    
    def calculate_board_points(self):
        points = self.board.get_points()
        if points % 5 == 0:
            return points // 5
        return 0
    
    def score(self, player, points):
        self.scores[player.name] += points
        return

    def draw_board(self):
        if self.display_on:
            self.display.window.fill((120, 120, 120))
            self.display.draw_tiles(self.players)
            self.display.draw_board(self.board)
            self.display.draw_scores(self.scores, self.players)
            self.display.create_play_button()
            self.display.create_draw_button()
            pygame.display.flip()

    def handle_events(self):
        if self.display_on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        x, y = pos
        tile_selected = self.display.handle_tile_click(self.current_player, x, y)
        edge_selected = self.display.handle_edge_click(self.board, x, y)
        play_button = self.display.play_button_rect
        if play_button.collidepoint(x, y) and tile_selected:
            self.handle_play(tile_selected, edge_selected)
        draw_button = self.display.draw_button_rect
        if draw_button.collidepoint(x, y):
            self.handle_draw()

            
    def handle_draw(self):
        if len(self.boneyard.tiles) == 1:
            # Cant draw last tile in bone yard
            self.next_turn()
            return
        if self.current_player.get_moves(self.board) == []:
            self.current_player.draw(self.boneyard)
        else:
            print("You have a valid move, you can't draw")


    def handle_play(self, tile_selected, edge_selected):
        player = self.current_player
        if player.play(self.board, tile_selected, edge_selected):
            board_points = self.calculate_board_points()
            self.score(self.current_player, board_points)
            self.next_turn()
            tile_selected.selected = False
            if edge_selected:
                edge_selected.chosen = False

    def handle_agent_play(self):
        move = self.current_player.get_action(self.board)
        if move is not None:
            self.current_player.play(self.board, move)
            board_points = self.calculate_board_points()
            self.score(self.current_player, board_points)
            self.next_turn()
        else:
            self.handle_draw()

    def next_turn(self):
        if self.round_over():
            deadwood_points = self.calculate_deadwood_points()
            self.score(self.current_player, deadwood_points)
            return
        idx = self.players.index(self.current_player)
        if idx == len(self.players) - 1:
            self.current_player = self.players[0]
        else:
            self.current_player = self.players[idx + 1]

    def is_stalemate(self):
        if len(self.boneyard.tiles) == 1:
            for player in self.players:
                if player.get_moves(self.board) != []:
                    return False
            return True
        
    def calculate_deadwood_points(self):
        deadwood_points = 0
        for player in self.players:
            deadwood_points += player.deadwood()
        return round(deadwood_points / 5)

    def round_over(self):
        for player in self.players:
            if len(player.hand) == 0:
                return True
        
    def game_over(self):
        scores = [self.scores[player.name] for player in self.players]
        # if the scores are not the same and one player has more than 61 points and the round is over
        if len(set(scores)) != 1 and max(scores) > 60 and self.round_over():
            return True
        return False
    
    def announce_winner(self):
        scores = [self.scores[player.name] for player in self.players]
        winner = self.players[scores.index(max(scores))]
        print("The winner is:", winner.name)
        print("Scores:", self.scores)
        self.draw_board()

    def play(self):
        self.deal()
        rounds = 0
        while not self.game_over():
            self.draw_board()
            if (self.round_over() or self.is_stalemate()) and not self.game_over():
                self.reset()
                rounds += 1
            if self.current_player.is_agent:
                self.handle_agent_play()
            self.handle_events()
        print("Rounds:", rounds)
        self.announce_winner()
