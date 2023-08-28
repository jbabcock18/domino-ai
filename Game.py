import pygame
import sys
from Domino import *

# Initialize Pygame
pygame.init()

# Set up the window
pygame.display.set_caption("Dominoes")
window_size = (1600, 1200)
window = pygame.display.set_mode(window_size)

# Define a function to draw a tile
def draw_tile(tile, x, y):
    pygame.draw.rect(window, (0, 0, 0), (x, y, 60, 30))
    pygame.draw.line(window, (255, 255, 255), (x + 30, y), (x + 30, y + 30), 1)
    font = pygame.font.SysFont(None, 24)
    text_a = font.render(str(tile.a), True, (255, 255, 255))
    text_b = font.render(str(tile.b), True, (255, 255, 255))
    window.blit(text_a, (x + 10, y + 5))
    window.blit(text_b, (x + 40, y + 5))

def draw_vertical_tile(tile, x, y):
    pygame.draw.rect(window, (0, 0, 0), (x, y, 30, 60))
    pygame.draw.line(window, (255, 255, 255), (x, y + 30), (x + 30, y + 30), 1)
    font = pygame.font.SysFont(None, 24)
    text_a = font.render(str(tile.a), True, (255, 255, 255))
    text_b = font.render(str(tile.b), True, (255, 255, 255))
    window.blit(text_a, (x + 10, y + 10))
    window.blit(text_b, (x + 10, y + 40))

def draw_tile_r(tile, x, y, visited, verticle):
    # Check if the tile has been visited to prevent infinite recursion
    if tile in visited:
        return
    visited.add(tile)

    if tile.is_double():
        verticle = not verticle
    # Draw the current tile
    if verticle:
        draw_vertical_tile(tile, x, y)
    else:
        draw_tile(tile, x, y)

    # 15 is half the width of a tile
    # 35 is width of a tile + 5
    # 65 is height of a tile + 5
    # Recursively draw connected tile
    if tile.a_edge:
        if verticle:
            if tile.a_edge.is_double():
                draw_tile_r(tile.a_edge, x - 15, y - 35, visited, verticle)
            else:
                draw_tile_r(tile.a_edge, x, y - 65, visited, verticle)
        else:
            if tile.a_edge.is_double():
                draw_tile_r(tile.a_edge, x - 35, y - 15, visited, verticle)
            else:
                draw_tile_r(tile.a_edge, x - 65, y, visited, verticle)
    if tile.b_edge:
        if verticle:
            if tile.b_edge.is_double():
                draw_tile_r(tile.b_edge, x - 15, y + 65, visited, verticle)
            else:
                draw_tile_r(tile.b_edge, x, y + 65, visited, verticle)
        else:
            if tile.b_edge.is_double():
                draw_tile_r(tile.b_edge, x + 65, y - 15, visited, verticle)
            else:
                draw_tile_r(tile.b_edge, x + 65, y, visited, verticle)
    if tile.double_a:
        if not verticle:
            draw_tile_r(tile.double_a, x + 15, y - 65, visited, not verticle)
        else:
            draw_tile_r(tile.double_a, x - 65, y + 15, visited, not verticle)
    if tile.double_b:
        if not verticle:
            draw_tile_r(tile.double_b, x + 15, y + 35, visited, not verticle)
        else:
            draw_tile_r(tile.double_b, x + 35, y + 15, visited, not verticle)

def draw_board(board):
    visited = set()
    x = window_size[0] // 2
    y = window_size[1] // 2
    draw_tile_r(board.first_tile(), x, y, visited, False)

def draw_tiles(players):
    for i, tile in enumerate(players[0].hand):
        y = window_size[1] - 100
        draw_tile(tile, 200 + i * 70, y)

    for i, tile in enumerate(players[1].hand):
        draw_tile(tile, 200 + i * 70, 100)

# Create some sample tiles
boneyard = BoneYard()
boneyard.shuffle()
board = Board()
p1 = DominoPlayer(boneyard, board)
p2 = DominoPlayer(boneyard, board)
players = [p1, p2]
for i in range(5):
    for player in players:
        player.draw()

# Main game loop
p1.play(0, 0)
turn = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player = players[turn % 2]
    # print("Player", turn % 2 + 1, "move:")
    while len(player.get_moves()) == 0:
        if player.draw() == False:
            # Can't draw last tile
            break

    moves = player.get_moves()
    if len(moves) == 0:
        # Skip player
        turn += 1
        continue 
    else:
        player.play(moves[0][0], moves[0][1])
        turn += 1
        
    window.fill((255, 255, 255))
    draw_tiles(players)
    draw_board(board)
    # for tile in board.tiles:
    #     tile.show()

    pygame.display.flip()
    pygame.time.wait(300)
