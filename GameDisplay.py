import pygame
import sys
from Domino import *

class GameDisplay:
    def __init__(self, window_size=(1000, 800), tile_length=60):
        self.window_size = window_size
        self.window = pygame.display.set_mode(self.window_size)
        self.window.fill((255, 255, 255))
        self.tile_length = tile_length
        self.tile_width = self.tile_length // 2
        pygame.display.set_caption("Dominoes")
        pygame.init()

    # Define a function to draw a tile
    def draw_tile(self, tile, x, y):
        pygame.draw.rect(self.window, (0, 0, 0), (x, y, self.tile_length, self.tile_width))
        pygame.draw.line(self.window, (255, 255, 255), (x + self.tile_width, y), (x + self.tile_width, y + self.tile_width), 1)
        font = pygame.font.SysFont(None, 24)
        text_a = font.render(str(tile.a), True, (255, 255, 255))
        text_b = font.render(str(tile.b), True, (255, 255, 255))
        self.window.blit(text_a, (x + 10, y + 5))
        self.window.blit(text_b, (x + 40, y + 5))

    def draw_vertical_tile(self, tile, x, y):
        pygame.draw.rect(self.window, (0, 0, 0), (x, y, self.tile_width, self.tile_length))
        pygame.draw.line(self.window, (255, 255, 255), (x, y + self.tile_width), (x + self.tile_width, y + self.tile_width), 1)
        font = pygame.font.SysFont(None, 24)
        text_a = font.render(str(tile.a), True, (255, 255, 255))
        text_b = font.render(str(tile.b), True, (255, 255, 255))
        self.window.blit(text_a, (x + 10, y + 10))
        self.window.blit(text_b, (x + 10, y + 40))

    def draw_tile_r(self, tile, x, y, visited, verticle):
        # Check if the tile has been visited to prevent infinite recursion
        if tile in visited:
            return
        visited.add(tile)

        if tile.is_double():
            verticle = not verticle
        # Draw the current tile
        if verticle:
            self.draw_vertical_tile(tile, x, y)
        else:
            self.draw_tile(tile, x, y)

        gap = 5
        quarter_tile = self.tile_length // 4
        half_tile = self.tile_length // 2 + gap
        tile_length = self.tile_length + gap
        # Recursively draw connected tile
        if tile.a_edge:
            if verticle:
                if tile.a_edge.is_double():
                    self.draw_tile_r(tile.a_edge, x - quarter_tile, y - half_tile, visited, verticle)
                else:
                    self.draw_tile_r(tile.a_edge, x, y - tile_length, visited, verticle)
            else:
                if tile.a_edge.is_double():
                    self.draw_tile_r(tile.a_edge, x - half_tile, y - quarter_tile, visited, verticle)
                else:
                    self.draw_tile_r(tile.a_edge, x - tile_length, y, visited, verticle)
        if tile.b_edge:
            if verticle:
                if tile.b_edge.is_double():
                    self.draw_tile_r(tile.b_edge, x - quarter_tile, y + tile_length, visited, verticle)
                else:
                    self.draw_tile_r(tile.b_edge, x, y + tile_length, visited, verticle)
            else:
                if tile.b_edge.is_double():
                    self.draw_tile_r(tile.b_edge, x + tile_length, y - quarter_tile, visited, verticle)
                else:
                    self.draw_tile_r(tile.b_edge, x + tile_length, y, visited, verticle)
        if tile.double_a:
            if not verticle:
                self.draw_tile_r(tile.double_a, x + quarter_tile, y - tile_length, visited, not verticle)
            else:
                self.draw_tile_r(tile.double_a, x - tile_length, y + quarter_tile, visited, not verticle)
        if tile.double_b:
            if not verticle:
                self.draw_tile_r(tile.double_b, x + quarter_tile, y + half_tile, visited, not verticle)
            else:
                self.draw_tile_r(tile.double_b, x + half_tile, y + quarter_tile, visited, not verticle)

    def draw_board(self, board):
        if len(board.tiles) == 0:
            return
        x = self.window_size[0] // 2
        y = self.window_size[1] // 2
        visited = set()
        self.draw_tile_r(board.first_tile(), x, y, visited, False)
        self.draw_points(board)

    def draw_tiles(self, players):
        x_gap = self.tile_length + 10
        y_gap = self.tile_width + 10
        for i, tile in enumerate(players[0].hand):
            self.draw_tile(tile, 200 + i * x_gap, self.window_size[1] - 100)
        if len(players) >= 3:
            for i, tile in enumerate(players[1].hand):
                self.draw_tile(tile, 40, 200 + i * y_gap)
            for i, tile in enumerate(players[2].hand):
                self.draw_tile(tile, 200 + i * x_gap, 100)
        else:
            for i, tile in enumerate(players[1].hand):
                self.draw_tile(tile, 200 + i * x_gap, 100)
            
        if len(players) >= 4:
            for i, tile in enumerate(players[3].hand):
                self.draw_tile(tile, self.window_size[0] - 100, 200 + i * y_gap)

    def draw_points(self, board):
        points = board.get_points()
        font = pygame.font.SysFont(None, 32)
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        # Top middle of screen
        text_rect = text.get_rect(center=(self.window_size[0] // 2, 20))
        self.window.blit(text, text_rect)
