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
        self.selected = False
        self.chosen = False
        self.rect = pygame.Rect(0, 0, 0, 0)

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
    
    def value(self):
        return self.a + self.b
    
    def is_double(self):
        return self.a == self.b
    
    def is_full(self):
        return self.a_edge is not None and self.b_edge is not None
    
    def can_play(self, tile, verbose=False):
        # If no edges match, raise error
        if self.a != tile.a and self.a != tile.b and self.b != tile.a and self.b != tile.b:
            if verbose:
                print("No matching edges", self, tile)
            return False
        
        if self.is_double():
            if self.a_edge is not None and self.b_edge is not None and self.double_a is not None and self.double_b is not None:
                if verbose:
                    print("Double already full")
                return False
        else:
            # If matching edge is already full, raise error
            if (tile.a == self.a and self.a_edge is not None) or (tile.a == self.b and self.b_edge is not None):
                if verbose:
                    print("A edge already full")
                return False
            
            if tile.b == self.a and self.a_edge is not None or tile.b == self.b and self.b_edge is not None:
                if verbose:
                    print("B edge already full")
                return False
            
        return True

    def add_edge(self, tile, verbose=False):
        if self.can_play(tile, verbose=True):
            pass
        else:
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

        # Adding to first tile
        elif self.a_edge is None and self.b_edge is None:
            if tile.is_double() and self.a == tile.a:
                self.a_edge = tile
                tile.double_b = self
            elif tile.is_double() and self.b == tile.a:
                self.b_edge = tile
                tile.double_a = self
            elif self.a == tile.a:
                tile.flip()
                tile.b_edge = self
                self.a_edge = tile
            elif self.a == tile.b:
                self.a_edge = tile
                tile.b_edge = self
            elif self.b == tile.a:
                self.b_edge = tile
                tile.a_edge = self
            elif self.b == tile.b:
                tile.flip()
                tile.a_edge = self
                self.b_edge = tile

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
        if verbose:
            print("Played the", tile, "on the", self)
        return True

class BoneYard:
    def __init__(self):
        self.reset()
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.tiles)

    def draw(self):
        if len(self.tiles) == 1:
            return None
        return self.tiles.pop()
    
    def reset(self):
        self.tiles = []
        for i in range(7):
            for j in range(i, 7):
                self.tiles.append(Tile(i, j))
        self.shuffle()


class Board:
    def __init__(self):
        self.tiles = []
        self.edge_tiles = []

    def add_edge(self, edge_idx, tile):
        valid = True
        if len(self.edge_tiles) == 0:
            self.tiles.append(tile)
        else:
            valid = self.edge_tiles[edge_idx].add_edge(tile)
            if valid:
                self.tiles.append(tile)

        self.edge_tiles = [tile for tile in self.tiles if not tile.is_full()]
        return valid
    
    def is_empty(self):
        return len(self.tiles) == 0
    
    def reset(self):
        self.tiles = []
        self.edge_tiles = []
    
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

    def get_index(self, tile):
        for idx, t in enumerate(self.edge_tiles):
            if t == tile:
                return idx
        return 0

    def get_points(self):
        points = 0
        for tile in self.edge_tiles:
            # Uncapped double
            if tile.is_double() and (tile.double_b is None or tile.double_a is None):
                points += tile.a * 2
            # Capped double
            elif tile.is_double() and tile.double_b is not None and tile.double_a is not None:
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