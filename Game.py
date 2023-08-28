import pygame
import sys
from Domino import *
from GameDisplay import *

# Create some sample tiles
boneyard = BoneYard()
boneyard.shuffle()
board = Board()
p1 = DominoPlayer(boneyard, board)
p2 = DominoPlayer(boneyard, board)
p3 = DominoPlayer(boneyard, board)
p4 = DominoPlayer(boneyard, board)
players = [p1, p2]
for i in range(5):
    for player in players:
        player.draw()

# Main game loop
p1.play(0, 0)
turn = 1
game_over = False
display = GameDisplay()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    display.window.fill((255, 255, 255))
    display.draw_tiles(players)
    display.draw_board(board)
    pygame.display.flip()

    if game_over:
        continue
    player = players[turn % len(players)]
    while len(player.get_moves()) == 0:
        print("Player", turn % len(players) + 1, "has to draw")
        if player.draw() == False:
            # Can't draw last tile
            break
        display.draw_tiles(players)
        pygame.display.flip()

        pygame.time.wait(1000)

    moves = player.get_moves()
    if len(moves) == 0:
        # Skip turn (can't play or draw)
        turn += 1
        continue 
    else:
        player.play(moves[0][0], moves[0][1])
        turn += 1
        
    if len(player.hand) == 0:
        print("Player", turn % len(players) + 1, "is out!")
        game_over = True
    pygame.time.wait(1000)
