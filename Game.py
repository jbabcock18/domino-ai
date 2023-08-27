import pygame
import sys
from Domino import *

# Initialize Pygame
pygame.init()

# Set up the window
window_size = (800, 600)
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

    # Recursively draw connected tile
    if tile.b_edge:
        if verticle:
            if tile.b_edge.is_double():
                draw_tile_r(tile.b_edge, x - 15, y + 35, visited, verticle)
            else:
                draw_tile_r(tile.b_edge, x, y + 65, visited, verticle)
        else:
            if tile.b_edge.is_double():
                draw_tile_r(tile.b_edge, x + 35, y - 15, visited, verticle)
            else:
                draw_tile_r(tile.b_edge, x + 65, y, visited, verticle)
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
    # Playing off a double
    if tile.double_a:
        if not verticle:
            draw_tile_r(tile.double_a, x + 15, y - 65, visited, not verticle)
        else:
            draw_tile_r(tile.double_a, x - 65, y + 15, visited, not verticle)
    if tile.double_b:
        if not verticle:
            draw_tile_r(tile.double_b, x + 15, y + 65, visited, not verticle)
        else:
            draw_tile_r(tile.double_b, x + 65, y + 15, visited, not verticle)


# Create some sample tiles
boneyard = BoneYard()
# boneyard.shuffle()
board = Board()

p1 = DominoPlayer(boneyard, board)
for i in range(28):
    p1.draw()
p1.play(4, 0)
p1.play(3, 0)
p1.play(1, 1)
p1.play(1, 1)
p1.play(3, 1)
p1.play(2, 2)
p1.play(5, 1)
p1.play(6, 3)
p1.play(3, 3)
p1.play(9, 3)
p1.play(14, 3)
p1.play(16, 5)
p1.play(2, 3)

print("player hand")
p1.show()
print("board edges")
board.show_edges()

print("board tiles")
for idx, tile in enumerate(board.tiles):
    print(tile.show())

first_tile = board.first_tile()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    window.fill((255, 255, 255))
    visited = set()
    draw_tile_r(first_tile, 400, 300, visited, False)

    pygame.display.flip()
