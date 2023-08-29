import pygame
import sys
from Domino import *
from GameDisplay import *

class Game:
    def __init__(self, num_players=2):
        self.boneyard = BoneYard()
        self.boneyard.shuffle()
        self.board = Board()
        self.display = GameDisplay()
        self.players = []
        for i in range(num_players):
            self.players.append(DominoPlayer(self.boneyard, self.board))

    def deal(self):
        for player in self.players:
            for i in range(5):
                player.hand.append(self.boneyard.draw())

    def play(self):
        self.deal()
        tile_selected = None
        turn = 0
        while True:
            # Update turn
            player = self.players[turn % len(self.players)]
            player.turn = True
            for p in self.players:
                if p != player:
                    p.turn = False
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    tile_selected = self.display.handle_click(self.players, x, y)
                    if play_button_rect.collidepoint(x, y) and tile_selected:
                        # Handle the logic for playing the selected tile here
                        idx = player.get_index(tile_selected)
                        if player.play(idx, 0):
                            turn += 1
                            tile_selected.selected = False
                            tile_selected = None

            self.display.window.fill((220, 220, 220))

            self.display.draw_tiles(self.players)
            self.display.draw_board(self.board)
            play_button_rect = self.display.draw_play_button()

            pygame.display.flip()

game = Game()
game.play()