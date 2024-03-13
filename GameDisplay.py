import pygame
import sys
from Dominos import *

class GameDisplay:
    def __init__(self, window_size=(1600, 1000), tile_length=70):
        pygame.init()
        self.window_size = window_size
        self.tile_length = tile_length
        self.tile_width = self.tile_length // 2
        self.play_button_rect = None
        self.draw_button_rect = None

    def setup(self):
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Dominoes")
        pygame.display.update()

    def draw_pips(self, x, y, num_pips, pip_radius):
        if num_pips == 0:
            return
        positions = []
        # Define the pip positions dynamically based on num_pips and tile dimensions
        # Add your logic here to set the positions list
        center_dot = (self.tile_length // 4, self.tile_width // 2)
        bottom_left = (self.tile_length // 8, self.tile_width - self.tile_width // 4)
        bottom_right = (self.tile_length // 4 + self.tile_length // 8, self.tile_width - self.tile_width // 4)
        top_left = (self.tile_length // 8, self.tile_width // 4)
        top_right = (self.tile_length // 4 + self.tile_length // 8, self.tile_width // 4)
        center_bottom = (self.tile_length // 4, self.tile_width - self.tile_width // 4)
        center_top = (self.tile_length // 4, self.tile_width // 4)
        if num_pips == 1:
            positions.append(center_dot)
        elif num_pips == 2:
            positions.append(top_left)
            positions.append(bottom_right)
        elif num_pips == 3:
            positions.append(top_left)
            positions.append(center_dot)
            positions.append(bottom_right)
        elif num_pips == 4:
            positions.append(bottom_left)
            positions.append(bottom_right)
            positions.append(top_left)
            positions.append(top_right)
        elif num_pips == 5:
            positions.append(bottom_left)
            positions.append(bottom_right)
            positions.append(top_left)
            positions.append(top_right)
            positions.append(center_dot)
        elif num_pips == 6:
            positions.append(bottom_left)
            positions.append(bottom_right)
            positions.append(top_left)
            positions.append(top_right)
            positions.append(center_bottom)
            positions.append(center_top)

        for pos_x, pos_y in positions:
            pygame.draw.circle(self.window, (255, 255, 255), (x + pos_x, y + pos_y), pip_radius)

    def draw_verticle_pips(self, x, y, num_pips, pip_radius):
        if num_pips == 0:
            return
        positions = []
        # Define the pip positions dynamically based on num_pips and tile dimensions
        # Add your logic here to set the positions list
        center_dot = (self.tile_length // 4, self.tile_width // 2)
        bottom_left = (self.tile_length // 8, self.tile_width - self.tile_width // 4)
        bottom_right = (self.tile_length // 4 + self.tile_length // 8, self.tile_width - self.tile_width // 4)
        top_left = (self.tile_length // 8, self.tile_width // 4)
        top_right = (self.tile_length // 4 + self.tile_length // 8, self.tile_width // 4)
        center_left = (self.tile_length // 8, self.tile_width // 2)
        center_right = (self.tile_length // 4 + self.tile_length // 8, self.tile_width // 2)

        if num_pips == 1:
            positions.append(center_dot)
        elif num_pips == 2:
            positions.append(top_right)
            positions.append(bottom_left)
        elif num_pips == 3:
            positions.append(top_right)
            positions.append(center_dot)
            positions.append(bottom_left)
        elif num_pips == 4:
            positions.append(bottom_left)
            positions.append(bottom_right)
            positions.append(top_left)
            positions.append(top_right)
        elif num_pips == 5:
            positions.append(bottom_left)
            positions.append(bottom_right)
            positions.append(top_left)
            positions.append(top_right)
            positions.append(center_dot)
        elif num_pips == 6:
            positions.append(bottom_left)
            positions.append(bottom_right)
            positions.append(top_left)
            positions.append(top_right)
            positions.append(center_left)
            positions.append(center_right)

        for pos_x, pos_y in positions:
            pygame.draw.circle(self.window, (255, 255, 255), (x + pos_x, y + pos_y), pip_radius)

    def draw_tile(self, tile, x, y):
        color = (0, 0, 0)
        if tile.selected:
            color = (0, 128, 0)
        elif tile.chosen:
            color = (128, 0, 0)
        # Draw rounded rectangle
        tile.rect = (pygame.Rect(x, y, self.tile_length, self.tile_width))
        pygame.draw.rect(self.window, color, (x, y + 5, self.tile_length, self.tile_width - 10))
        pygame.draw.rect(self.window, color, (x + 5, y, self.tile_length - 10, self.tile_width))
        pygame.draw.circle(self.window, color, (x + 5, y + 5), 5)
        pygame.draw.circle(self.window, color, (x + self.tile_length - 5, y + 5), 5)
        pygame.draw.circle(self.window, color, (x + 5, y + self.tile_width - 5), 5)
        pygame.draw.circle(self.window, color, (x + self.tile_length - 5, y + self.tile_width - 5), 5)
        
        # Draw line in the middle
        pygame.draw.line(self.window, (255, 255, 255), (x + self.tile_width, y), (x + self.tile_width, y + self.tile_width), 1)
        
        # Draw pips
        pip_radius = self.tile_length / 22 
        self.draw_pips(x, y, tile.a, pip_radius)
        self.draw_pips(x + self.tile_width, y, tile.b, pip_radius)

    def draw_vertical_tile(self, tile, x, y):
        color = (0, 0, 0)
        if tile.selected:
            color = (0, 128, 0)
        elif tile.chosen:
            color = (128, 0, 0)
        # Draw rounded rectangle
        tile.rect = (pygame.Rect(x, y, self.tile_width, self.tile_length))
        pygame.draw.rect(self.window, color, (x + 5, y, self.tile_width - 10, self.tile_length))
        pygame.draw.rect(self.window, color, (x, y + 5, self.tile_width, self.tile_length - 10))
        pygame.draw.circle(self.window, color, (x + 5, y + 5), 5)
        pygame.draw.circle(self.window, color, (x + self.tile_width - 5, y + 5), 5)
        pygame.draw.circle(self.window, color, (x + 5, y + self.tile_length - 5), 5)
        pygame.draw.circle(self.window, color, (x + self.tile_width - 5, y + self.tile_length - 5), 5)

        # Draw line in the middle
        pygame.draw.line(self.window, (255, 255, 255), (x, y + self.tile_width), (x + self.tile_width, y + self.tile_width), 1)

        # Draw pips
        pip_radius = self.tile_length / 22  # or some value depending on tile dimensions
        self.draw_verticle_pips(x, y, tile.a, pip_radius)
        self.draw_verticle_pips(x, y + self.tile_width, tile.b, pip_radius)


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

    def handle_tile_click(self, player, x, y):
        for tile in player.hand:
            if tile.rect.collidepoint(x, y):
                tile.selected = not tile.selected
                # all other tiles are unselected
                for other_tile in player.hand:
                    if other_tile != tile:
                        other_tile.selected = False
        # return the selected tile
        for tile in player.hand:
            if tile.selected:
                return tile
                
    def handle_edge_click(self, board, x, y):
        for tile in board.edge_tiles:
            if tile.rect.collidepoint(x, y):
                tile.chosen = not tile.chosen
                # all other tiles are unselected
                for other_tile in board.edge_tiles:
                    if other_tile != tile:
                        other_tile.chosen = False
        # return the selected tile
        for tile in board.edge_tiles:
            if tile.chosen:
                return tile

    def draw_tiles(self, players):
        x_gap = self.tile_length + 10
        y_gap = self.tile_width + 10
        for i, tile in enumerate(players[0].hand):
            x_pos = 200 + i * x_gap
            y_pos = self.window_size[1] - 100
            self.draw_tile(tile, x_pos, y_pos)
            tile.rect = (pygame.Rect(x_pos, y_pos, self.tile_length, self.tile_width))
        if len(players) >= 3:
            for i, tile in enumerate(players[1].hand):
                x_pos = 40
                y_pos = 200 + i * y_gap
                self.draw_tile(tile, x_pos, y_pos)
                tile.rect = (pygame.Rect(x_pos, y_pos, self.tile_length, self.tile_width))
            for i, tile in enumerate(players[2].hand):
                x_pos = 200 + i * x_gap
                y_pos = 100
                self.draw_tile(tile, x_pos, y_pos)
                tile.rect = (pygame.Rect(x_pos, y_pos, self.tile_length, self.tile_width))
        else:
            for i, tile in enumerate(players[1].hand):
                x_pos = 200 + i * x_gap
                y_pos = 100
                self.draw_tile(tile, x_pos, y_pos)
                tile.rect = (pygame.Rect(x_pos, y_pos, self.tile_length, self.tile_width))
        if len(players) >= 4:
            for i, tile in enumerate(players[3].hand):
                x_pos = self.window_size[0] - 100
                y_pos = 200 + i * y_gap
                self.draw_tile(tile, x_pos, y_pos)
                tile.rect = (pygame.Rect(x_pos, y_pos, self.tile_length, self.tile_width))

    def draw_points(self, board):
        points = board.get_points()
        font = pygame.font.SysFont(None, 32)
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        # Top middle of screen
        text_rect = text.get_rect(center=(self.window_size[0] // 2, 20))
        self.window.blit(text, text_rect)

    def create_play_button(self):
        button_color = (0, 128, 0)
        x, y, width, height = self.window_size[0] - 100, self.window_size[1] - 50, 80, 40
        pygame.draw.rect(self.window, button_color, (x, y, width, height))
        font = pygame.font.SysFont(None, 24)
        text = font.render("Play", True, (255, 255, 255))
        self.window.blit(text, (x + 20, y + 10))
        self.play_button_rect = pygame.Rect(x, y, width, height)

    def create_draw_button(self):
        button_color = (0, 128, 128)
        x, y, width, height = self.window_size[0] - 200, self.window_size[1] - 50, 80, 40
        pygame.draw.rect(self.window, button_color, (x, y, width, height))
        font = pygame.font.SysFont(None, 24)
        text = font.render("Draw", True, (255, 255, 255))
        self.window.blit(text, (x + 20, y + 10))
        self.draw_button_rect = pygame.Rect(x, y, width, height)

    def draw_scores(self, scores, players):
        font = pygame.font.SysFont(None, 32)
        # Top of screen, each player left to right
        i = 0
        for k, v in scores.items():
            text = font.render("{}: {}".format(k, int(v)), True, (0, 0, 0))
            text_rect = text.get_rect(center=(200 + (i*200), 20))
            self.window.blit(text, text_rect)
            i += 1