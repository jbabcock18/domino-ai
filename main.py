from Game import Game
from Dominos import Board, BoneYard
from GameDisplay import GameDisplay
from agents.DumbAgent import DumbAgent
from agents.SimpleAgent import SimpleAgent
from Player import DominoPlayer

def main():
    board = Board()
    boneyard = BoneYard()
    p1 = SimpleAgent()
    p2 = SimpleAgent("Jerry")
    players = [p1, p2]
    game = Game(players, board, boneyard, display_on=False)
    game.play()


if __name__ == "__main__":
    main()