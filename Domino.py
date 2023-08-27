import random    
import pygame

class Tile:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.a_edge = None
        self.b_edge = None
        self.double_a = None
        self.double_b = None

    def __str__(self):
            return f"[{self.a}|{self.b}]"
    
    def __eq__(self, __value: object) -> bool:
        if self.a == __value.a and self.b == __value.b:
            return True
        elif self.a == __value.b and self.b == __value.a:
            return True
        else:
            return False
        
    def __hash__(self):
        return hash((self.a, self.b))
    
    def flip(self):
        self.a, self.b = self.b, self.a
    
    def show(self):
        print("a:", self.a)
        print("b:", self.b)
        print("a_edge:", self.a_edge)
        print("b_edge:", self.b_edge)
        print("double_a:", self.double_a)
        print("double_b:", self.double_b)
        print()
    
    def is_double(self):
        return self.a == self.b
    
    def is_full(self):
        return self.a_edge is not None and self.b_edge is not None

    def add_edge(self, tile):
        # If no edges match, raise error
        if self.a != tile.a and self.a != tile.b and self.b != tile.a and self.b != tile.b:
            print("No matching edges", self, tile)
            return False
        
        if self.is_double():
            if self.a_edge is not None and self.b_edge is not None and self.double_a is not None and self.double_b is not None:
                print("Double already full")
                return False
        else:
            # If matching edge is already full, raise error
            if (tile.a == self.a and self.a_edge is not None) or (tile.a == self.b and self.b_edge is not None):
                print("A edge already full")
                return False
            
            if tile.b == self.a and self.a_edge is not None or tile.b == self.b and self.b_edge is not None:
                print("B edge already full")
                return False
        
        # Adding to double as first tile
        if self.is_double() and self.double_a is None:
            # Always start with b
            if tile.a == self.a:
                tile.flip()
            tile.b_edge = self
            self.double_a = tile

        # Capping a double
        elif self.is_double() and self.double_b is None: #and self.double_a is not None
            # Always cap with a
            if tile.b == self.b:
                tile.flip()
            tile.a_edge = self
            self.double_b = tile

        # Adding to an a_edge 
        elif self.a_edge is None:
            if tile.is_double():
                tile.double_b = self
            else:
                # Set self.a_edge to tile.b_edge, always
                if tile.a == self.a:
                    tile.flip()
                tile.b_edge = self
            self.a_edge = tile

        # Adding to a b_edge
        elif self.b_edge is None:
            if tile.is_double():
                tile.double_a = self
            else:
                # Set self.b_edge to tile.a_edge, always
                if tile.b == self.b:
                    tile.flip()
                tile.a_edge = self
            self.b_edge = tile
        
        print("Played the", tile, "on the", self)
        return True

        
class Board:
    def __init__(self):
        self.tiles = []
        self.edge_tiles = []

    def add_edge(self, edge_idx, tile):
        valid = True
        if len(self.edge_tiles) == 0:
            self.tiles.append(tile)
            print("First tile:", tile)
        else:
            valid = self.edge_tiles[edge_idx].add_edge(tile)
            if valid:
                self.tiles.append(tile)

        self.edge_tiles = [tile for tile in self.tiles if not tile.is_full()]
        return valid
    
    def first_tile(self):
        return self.tiles[0]

    def show_tiles(self):
        for tile in self.tiles:
            print(tile)

    def show_edges(self):
        for idx, tile in enumerate(self.edge_tiles):
            print(idx, tile)

    def show_details(self):
        for tile in self.tiles:
            tile.show()        

    def get_points(self):
        points = 0
        for tile in self.edge_tiles:
            # Uncapped double
            if tile.is_double() and tile.double_cap is None:
                points += tile.a * 2
            # Capped double
            elif tile.is_double() and tile.double_cap is not None:
                continue
            # First tile
            elif tile.a_edge is None and tile.b_edge is None:
                points += tile.a + tile.b
            # Regular edge
            elif tile.a_edge is None:
                points += tile.a
            elif tile.b_edge is None:
                points += tile.b
        return points

class BoneYard:
    def __init__(self):
        self.tiles = []
        for i in range(7):
            for j in range(i, 7):
                self.tiles.append(Tile(i, j))

    def shuffle(self):
        random.shuffle(self.tiles)

    def draw(self):
        return self.tiles.pop()

class DominoPlayer:
    def __init__(self, bone_yard, board):
        self.hand = []
        self.bone_yard = bone_yard
        self.board = board

    def draw(self):
        self.hand.append(self.bone_yard.draw())

    def show(self):
        for idx, tile in enumerate(self.hand):
            print(idx, tile)

    def play(self, tile_idx, edge_idx):
        tile = self.hand[tile_idx]
        valid = self.board.add_edge(edge_idx, tile)
        if valid:
            self.hand.pop(tile_idx)
        

    def get_remaining_tiles(self):
        remaining = []
        for i in range(7):
            for j in range(i, 7):
                remaining.append(Tile(i, j))
        for tile in self.hand:
            remaining.remove(tile)
        for tile in self.board.tiles:
            remaining.remove(tile)
        return remaining
        
