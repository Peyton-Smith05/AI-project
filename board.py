"""
FEN Notation:
* example of starting state fen string
    * 'rheakaehr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RHEAKAEHR w - - 0 1'

* / : indicate next rank
* numerical value 1-9 : indicates number of empty squares between pieces
* w | b : indicates turn
* - : indicates filler for notation in western chess
* second to last value is number of half moves since last capture (if reaches 60 game ends in draw)
* last value is number of full moves (full move means increments after both white and black move)

* Upper Case for White, Lower case for black
    * King/General: K/k
    * Advisor: A/a
    * Elephant: E/e
    * Rook/Chariot: R/r
    * Cannon: C/c
    * Horse/Knight: H/h
    * Pawn: P/p

"""

from move import Move
from piece import *

"""

@:var state {array[90] of char} contains current state of board
@:var turn {char} w | b
@:var king_pos {int} integer position of the turn of current players king within state
                     (this will be needed for determining legal moves)
@:var half_moves {int} number of half moves since last capture. If == 60 then game ends in draw,
                       increments after white or black move
@:var full_moves {int} number of full moves

@:func __init__(self, fen) default constructor, calls helper function generateStringFromFen()

TODO:

@:func generateValidMoves()
@:func evaluateBoardPos()
@:func checkForCheck(move: move.Move, turn: char): Helper function that analyzes a move and looks a half move further 
                                                   to see if that move puts themselves in check. Returns bool.
@:func validateMove(m: move.Move): General function to check if the move is psuedo legal


"""

# Mapping letters stored in Board state to Piece classes
PIECE_MAPPING = { "K":King, "A":Advisor, "E":Elephant, "H":Horse,
                  "R":Rook, "C":Cannon, "P":Pawn }


class Board:
    """
    Constructor from fen
    @:param fen {string} fen string that indicates the piece state, turn, and full move counter 
    @:return state {1d char array}, turn {bool}, half_moves {int}, and full_moves {int}
    """

    def __init__(self, fen, computer_color):
        self.computer_color = computer_color
        king = ''
        if computer_color == 'w':
            king = 'K'
        else:
            king = 'k'

        self.state = []
        parse = fen.split(" ")

        board_rows = parse[0]

        # Reverse inorder to match list order with rank and file system
        board_rows = board_rows[::-1]

        # Getting piece positions
        for x in range(len(board_rows)):
            if board_rows[x].isdigit():
                for i in range(int(board_rows[x])):
                    self.state.append("+")

            elif board_rows[x] == '/':
                continue

            else:
                if board_rows[x] == king:
                    self.king_pos = x
                self.state.append(board_rows[x])

        # Getting turn
        self.turn = parse[1]

        # Getting half moves
        self.half_moves = int(parse[4])

        # Getting full moves
        self.full_moves = int(parse[5])

    def __str__(self):
        count = 0
        board_str = ""
        for i in range(len(self.state)):
            if count != 8:
                board_str += (self.state[i] + " ")
                count += 1
            else:
                board_str += (self.state[i] + "\n")
                count = 0

        board_str += "\n"
        if self.turn == 'w':
            board_str += "White to move"
        else:
            board_str += "Black to move"

        return board_str

    def updateBoardFromMove(self, m: Move):

        # TODO: Validate move??

        # Swap places in list
        self.state[m.target] = self.state[m.start]
        self.state[m.start] = '+'

        # Update Turn
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'

    def isOccupied(self, file, rank):
        return self.state[(rank-1)*9 + (file-1)] != "+"

    def generateValidMoves(self, file, rank):
        """
        Given a single piece location, generate a list of pseudo-legal moves
        :@param file {int} vertical line on board, range={1..9}
        :@param rank {int} horizontal line on board, range={1..10}

        TODO: Account for special capture movement of Cannon
        TODO: Check for check and prevent movements
        TODO: Check for two kings facing each other directly
        """

        # List of pseudo-random moves
        moves = []

        # Identify piece occupying given location
        unknown_piece = self.state[(rank-1)*9 + (file-1)]
        piece = PIECE_MAPPING[unknown_piece.upper()]

        # Get the movement specification of the given piece
        vectors, any_dist, area = piece.get_move_vectors(self, file, rank, unknown_piece.islower())
        
        # Check the bounding area for the given piece
        if area is not None:
            min_file, max_file = area[0]
            min_rank, max_rank = area[1]
        else:
            min_file, max_file = 1, 9
            min_rank, max_rank = 1, 10

        # Generate pseudo-legal moves
        for vector_sequence in vectors:

            new_file, new_rank = file, rank
            outside = False
            occupied = False
            should_advance = True
            
            # This loop allows to model moves of any distance along an axis
            while should_advance and not outside and not occupied:

                # For all pieces, apart for Horse this will run once
                # (Horse has a two-stage move)
                for vector in vector_sequence:

                    # 1. Compute resulting new position
                    new_file += vector[0]
                    new_rank += vector[1]
                    
                    # 2. Check if new location is within bounds
                    if not (min_file <= new_file <= max_file) or not (min_rank <= new_rank <= max_rank):
                        # Outside the bounding area, check next option
                        outside = True
                        break

                    # 3. Check if new location is occupied
                    occupied = self.isOccupied(new_file, new_rank)

                # 4. Create a move and add to list
                if not occupied and not outside:
                    move = Move((file, rank), (new_file, new_rank))
                    print(move)
                    moves.append(move)

                # If the given piece can move any distance along an axis (e.g. Cannon or Rook)
                # the loop should continue until an obstruction is encountered or end of board reached
                should_advance = any_dist

        return moves
            




        








