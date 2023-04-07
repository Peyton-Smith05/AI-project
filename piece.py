from abc import (ABC, abstractmethod)
import math

class Piece(ABC):
    """
    Abstract class for a piece.
    Each piece inherits from the class and implements methods below.

    All methods are static, meaning that no objects have to be instantiated saving on runtime and memory.
    """
    
    @staticmethod
    @abstractmethod
    def get_move_vectors(file, rank, red_side):
        """
        Given currrent location of the piece return the possible movement vectors for the given piece, i.e. ways in which the current piece can move, assuming there are no obstructions.

        :@param file, rank {int} current file and rank of the piece
        :@param red_side {bool} is given piece red (bottom player)

        :@return move_vectors {[[(int, int)]]}
        1. For single-step pieces - a list of singleton lists of tuples representing movement vectors, or
        2. For double-step pieces (e.g. Horse) - a list of lists of two tuples representing subsequent movement vectors.

        :@return any_dist {bool} can the piece move any distance along the specified vector

        :@return area {[(int, int), (int, int)]} allowed movement area for a given piece in the form [(min_file, max_file), (min_rank, max_rank)] 
        """
        pass

    @classmethod
    def get_value(cls, file=None, rank=None, red_side=None):
        """
        Given currrent location of the piece return the value of the piece

        :@param file, rank {int} current file and rank of the piece
        :@param red_side {bool} is given piece red (bottom player)

        :@return value {float}
        """
        return cls.value



# Implementation classes for each piece:

class King(Piece):
    # Orthogonal movements
    move_vectors = [[(1,0)],[(-1,0)],[(0,1)],[(0,-1)]]
    # King's value is infinity, for this purposes an arbitrarily high value
    value = 100000

    @staticmethod
    def get_move_vectors(file, rank, red_side):
        if red_side:
            palace = [(4,6),(8,10)]
        else:
            palace = [(4,6),(1,3)]

        return King.move_vectors, False, palace

class Advisor(Piece):
    # Diagonal movements
    move_vectors = [[(1,1)],[(1,-1)],[(-1,1)],[(-1,-1)]]
    value = 2

    @staticmethod
    def get_move_vectors(file, rank, red_side):
        if red_side:
            palace = [(4,6),(8,10)]
        else:
            palace = [(4,6),(1,3)]

        return Advisor.move_vectors, False, palace

class Elephant(Piece):
    # Diagonal movements
    move_vectors = [[(2,2)],[(2,-2)],[(-2,2)],[(-2,-2)]]
    value = 2

    @staticmethod
    def get_move_vectors(file, rank, red_side):
        if red_side:
            river_side = [(1,9),(6,10)]
        else:
            river_side = [(1,9),(1,5)]

        return Elephant.move_vectors, False, river_side

class Horse(Piece):
    # One orthogonal movement, followed by one diagonal
    move_vectors = [[(1,0),(1,1)], [(1,0),(1,-1)],
                    [(-1,0),(-1,1)], [(-1,0),(-1,-1)],
                    [(0,1),(1,1)], [(0,1),(-1,1)],
                    [(0,-1),(1,-1)], [(0,-1),(-1,-1)]]
    value = 4

    @staticmethod
    def get_move_vectors(file, rank, red_side):
        return Horse.move_vectors, False, None

class Rook(Piece):
    # Any orthogonal movement
    move_vectors = [[(1,0)],[(-1,0)],[(0,1)],[(0,-1)]]
    value = 9

    @staticmethod
    def get_move_vectors(file, rank, red_side):
        return Rook.move_vectors, True, None

class Cannon(Piece):
    # Any orthogonal movement
    move_vectors = [[(1,0)],[(-1,0)],[(0,1)],[(0,-1)]]
    value = 4.5

    @staticmethod
    def get_move_vectors(file, rank, red_side):
        return Cannon.move_vectors, True, None

class Pawn(Piece):
    # Forward movement up to river
    # Forward and side movement after river crossed
    value_before_river = 1
    value_after_river = 2

    @staticmethod
    def get_move_vectors(file, rank, red_side):
        move_vectors = None

        if red_side:
            # River crossed
            if rank <= 5:
                move_vectors = [[(0,-1)], [(1,0)], [(-1,0)]]
            # River not crossed
            else:
                move_vectors = [[(0,-1)]]
        else:
            # River crossed
            if rank >= 6:
                move_vectors = [[(0,1)], [(1,0)], [(-1,0)]]
            # River not crossed
            else:
                move_vectors = [[(0,1)]]

        return move_vectors, False, None

    @classmethod
    def get_value(cls, file=None, rank=None, red_side=None):
        if red_side:
            # River crossed
            if rank <= 5:
                return Pawn.value_after_river
            # River not crossed
            else:
                return Pawn.value_before_river
        else:
            # River crossed
            if rank >= 6:
                return Pawn.value_after_river
            # River not crossed
            else:
                return Pawn.value_before_river