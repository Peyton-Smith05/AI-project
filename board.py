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

# Proprietary code
import random
from move import Move
from piece import *

# Packages and libraries
from copy import deepcopy

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

@:func validateMove(m: move.Move): General function to check if the move is psuedo legal - This can probably be dealt with by comparing user input to the output of generateValidMoves()

@:func checkForGameEnd()
Check the current board to see if game has ended:
1. Check-mate - is_check() and all valid moves cause check also
2. Repeated move three times
3. Set number of turns passed

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

        if (self.computer_color == 'b'):
            self.player_pieces = [[1,10], [2,10], [3,10], [4,10], [5,10], [6,10], [7,10], [8,10], [9,10], [2,8], [8,8], [1,7], [3,7], [5,7], [7,7], [9,7]]
            self.aipieces = [[1,1], [2,1], [3,1], [4,1], [5,1], [6,1], [7,1], [8,1], [9,1], [2,3], [8,3], [1,4], [3,4], [5,4], [7,4], [9,4]]
        elif (self.computer_color == 'w'):   
            self.player_pieces =  [[1,1], [2,1], [3,1], [4,1], [5,1], [6,1], [7,1], [8,1], [9,1], [2,3], [8,3], [1,4], [3,4], [5,4], [7,4], [9,4]]
            self.aipieces = [[1,10], [2,10], [3,10], [4,10], [5,10], [6,10], [7,10], [8,10], [9,10], [2,8], [8,8], [1,7], [3,7], [5,7], [7,7], [9,7]]
        
        # Positions on the board that is under fire from the player pieces (AI will take into account these threats for move ordering)
        self.userthreats = set()
        # Positions on the board that is under fire from the AI pieces (Player will take into account these threats for move ordering)
        self.aithreats = set()
        # Populate both self.userthreats and self.aithreats on init based on intial aipieces and player_pieces positions
        self.ai_threat()
        self.user_threat()
    
    
    
    def __str__(self):
        count = 0
        board_str = "\n          BLACK              "
        board_str += "\n    1 2 3 4 5 6 7 8 9\n\n1   "
        rank = 1
        for i in range(len(self.state)):
            if count != 8:
                board_str += (self.state[i] + " ")
                count += 1
            else:
                rank += 1
                board_str += (self.state[i] + "\n")
                if rank < 10:
                    board_str += (str(rank) + "   ")
                elif rank == 10:
                    board_str += (str(rank) + "  ")

                count = 0

        board_str += "\n          WHITE              \n"
        board_str += "\n"
        if self.turn == 'w':
            board_str += "White to move"
        else:
            board_str += "Black to move" 

        return board_str
    
    
    # Get every position on the board that is under fire from the player pieces (threats that the AI have to be aware of)
    def ai_threat(self):
        temp = []
        self.userthreats.clear()
        for rank in range(1, 10+1):
            for file in range(1, 9+1):
                for pieces in self.player_pieces:
                    if (pieces[0] == file and pieces[1] == rank):
                        temp += Board.generate_pseudo_valid_moves_threats(self.state, file, rank)
        for move in temp:
            self.userthreats.add((move.target[0],move.target[1]))

    # Get every position on the board that is under fire from the AI pieces (threats that the player(user) have to be aware of)
    def user_threat(self):
        temp = []
        self.aithreats.clear()
        for rank in range(1, 10+1):
            for file in range(1, 9+1):
                for pieces in self.aipieces:
                    if (pieces[0] == file and pieces[1] == rank):
                        temp += Board.generate_pseudo_valid_moves_threats(self.state, file, rank)
        for move in temp:
            self.aithreats.add((move.target[0],move.target[1]))

    def updateBoardFromMove(self, m: Move):
          
        # Update positions of ai pieces or player pieces

        if (self.turn != self.computer_color):
            for i in self.player_pieces:
                if (i[0] == m.start[0] and i[1] == m.start[1]):
                    i[0] = m.target[0]
                    i[1] = m.target[1]
                    break
            for x in self.aipieces:
                if (x[0] == m.target[0] and x[1] == m.target[1]):
                    self.aipieces.remove(x)
                    break
        else:
            for i in self.aipieces:
                if (i[0] == m.start[0] and i[1] == m.start[1]):
                    i[0] = m.target[0]
                    i[1] = m.target[1]
                    break
            for x in self.player_pieces:
                if (x[0] == m.target[0] and x[1] == m.target[1]):
                    self.player_pieces.remove(x)
                    break
                

        # Swap places in list 

        self.state[(m.target[1]-1)*9 + (m.target[0]-1)] = self.state[(m.start[1]-1)*9 + (m.start[0]-1)]
        self.state[(m.start[1]-1)*9 + (m.start[0]-1)] = '+'

        # Update aithreats or userthreats list

        if (self.turn != self.computer_color):
            self.ai_threat()
        else:
            self.user_threat()

        # Update Turn
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'
    
    

    def checkForEndGame(self):
        # TODO: Add other conditions for game end
        # Check if King is at check
        for (side, name) in [(True, "White"), (False, "black")]:
            if (Board.is_check(self.state, side)):
                # Check if King can escape check
                position = Board.find_king(self.state, side)
                moves = Board.generate_pseudo_valid_moves(self.state, position[0], position[1])
                # Checkmate
                print()
                if len(moves) == 0:
                    print(name, " IS IN CHECKMATE. END OF THE GAME")
                    return True, name
                else:
                    print(name, " IS IN CHECK")
        return False, ""
            
    
    def simulateMove(self, move):
        return Board.simulate_move(self.state, move)

    @staticmethod
    def simulate_move(board, move):
        # Get the moving piece
        piece = board[(move.start[1]-1)*9 + (move.start[0]-1)]
        # Deep copy the current state of the board - potentially inefficient
        simulated_board = deepcopy(board)
        # Simulate the given move
        simulated_board[(move.start[1]-1)*9 + (move.start[0]-1)] = "+"
        simulated_board[(move.target[1]-1)*9 + (move.target[0]-1)] = piece
        return simulated_board

    def generateValidMoves(self, file, rank):
        """
        Given a single piece location, generate a list of all valid moves
        :@param file {int} vertical line on board, range={1..9}
        :@param rank {int} horizontal line on board, range={1..10}

        :@return moves {[Move]} list of valid moves
        """

        # If given location does not have a piece, no moves generated
        
        piece = self.state[(rank-1)*9 + (file-1)]
        if piece == "+":
            return []
        # Red piece
        
        elif piece.islower():
            red_side = True

        # Black piece
        else:
            red_side = False
        
        if self.turn == 'b' and red_side == True:
            return []
        
        if self.turn == 'r' and red_side == False:
            return []

        # 1. Generate pseudo-legal moves
        moves = Board.generate_pseudo_valid_moves(self.state, file, rank)
        
        # 2. Check for two kings facing each other directly
        moves = list(filter(lambda move: not Board.kings_facing(self.simulateMove(move)), moves))

        # 3. Check for check 
        moves = list(filter(lambda move: not Board.is_check(self.simulateMove(move), red_side), moves))

        return moves

    @staticmethod
    def generate_pseudo_valid_moves(board, file, rank):
        """
        Given a board state and a single piece location, generate a list of pseudo-legal moves
        :@param file {int} vertical line on board, range={1..9}
        :@param rank {int} horizontal line on board, range={1..10}

        Static function allowing to generate moves for the potential board states

        :@return moves {[Move]} list of pseudo-legal moves
        """

        # List of pseudo-legal moves
        moves = []

        # Identify piece occupying given location
        unknown_piece = board[(rank-1)*9 + (file-1)] 
        piece = PIECE_MAPPING[unknown_piece.upper()]

        # Get the movement specification of the given piece 
        vectors, any_dist, area = piece.get_move_vectors(file, rank, unknown_piece.islower()) 
        
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

            # Whether the last considered move should be disqualified
            disqualified = False
            # Whether the current sequence of move should be stopped
            # e.g. If way obstructed, do not consider the remaining positions
            halt = False

            capture = False
            cannon_platform = False
            should_advance = True
            
            # This loop allows to model moves of any distance along an axis
            while should_advance and not halt:

                # For all pieces, apart for Horse this will run once
                # (Horse has a two-stage move)
                for vector in vector_sequence:

                    # 1. Compute resulting new position
                    new_file += vector[0]
                    new_rank += vector[1]
                    
                    # 2. Check if new location is within bounds
                    if not (min_file <= new_file <= max_file) or not (min_rank <= new_rank <= max_rank):
                        # Outside the bounding area, check next option
                        disqualified = True
                        halt = True
                        break

                    # 3. Check if new location is occupied
                    occupied, friendly = Board.is_occupied(board, new_file, new_rank, unknown_piece)

                    # Occupied by friendly piece
                    if occupied and friendly:
                        disqualified = True
                        halt = True
                    # Occupied by opponent piece, is a single-step move, and piece is not Cannon
                    elif occupied and vector == vector_sequence[-1] and piece != Cannon:
                        disqualified = False
                        capture = True
                        halt = True
                    # Occupied by opponent piece and is the first-step of a two-step Horse move
                    elif occupied:
                        disqualified = True
                        halt = True

                    # Special Case: Cannon Capture
                    # If halted, and not reached end of board, 
                    # Cannon has encountered a piece it can use as a 'platform'
                    # Check if there is an opponent piece on the axis past the 'platform'
                    if piece == Cannon and occupied:
                        # Cannon platform encountered
                        if not cannon_platform:
                            cannon_platform = True
                            halt = False
                        # Enemy piece encountered after platform, can capture
                        elif cannon_platform and not friendly:
                            disqualified = False
                            capture = True
                            halt = True
                    # Cannon cannot move past obstruction, only capture
                    elif piece == Cannon and cannon_platform:
                        disqualified = True

                    if disqualified:
                        break

                # 4. Create a move and add to list
                if not disqualified:
                    move = Move((file, rank), (new_file, new_rank), capture)
                    moves.append(move)

                # If the given piece can move any distance along an axis (e.g. Cannon or Rook)
                # the loop should continue until an obstruction is encountered or end of board reached
                should_advance = any_dist

        return moves
    
    # To generate all positions that are being targeted by either the ai pieces or the player pieces 
    @staticmethod
    def generate_pseudo_valid_moves_threats(board, file, rank):
        """
        Given a board state and a single piece location, generate a list of pseudo-legal moves
        :@param file {int} vertical line on board, range={1..9}
        :@param rank {int} horizontal line on board, range={1..10}

        Static function allowing to generate moves for the potential board states

        :@return moves {[Move]} list of pseudo-legal moves
        """
        
        # List of pseudo-legal moves
        moves = []

        # Identify piece occupying given location
        unknown_piece = board[(rank-1)*9 + (file-1)] 
        piece = PIECE_MAPPING[unknown_piece.upper()]

        # Get the movement specification of the given piece 
        vectors, any_dist, area = piece.get_move_vectors(file, rank, unknown_piece.islower()) 
        
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

            # Whether the last considered move should be disqualified
            disqualified = False
            # Whether the current sequence of move should be stopped
            # e.g. If way obstructed, do not consider the remaining positions
            halt = False

            capture = False
            cannon_platform = False
            should_advance = True
            
            # This loop allows to model moves of any distance along an axis
            while should_advance and not halt:

                # For all pieces, apart for Horse this will run once
                # (Horse has a two-stage move)
                for vector in vector_sequence:

                    # 1. Compute resulting new position
                    new_file += vector[0]
                    new_rank += vector[1]
                    
                    # 2. Check if new location is within bounds
                    if not (min_file <= new_file <= max_file) or not (min_rank <= new_rank <= max_rank):
                        # Outside the bounding area, check next option
                        disqualified = True
                        halt = True
                        break

                    
                    # 3. Check if new location is occupied
                    occupied, friendly = Board.is_occupied(board, new_file, new_rank, unknown_piece)

                    # Occupied by friendly piece
                    if occupied and friendly:
                        disqualified = True
                        halt = True
                    # Occupied by opponent piece, is a single-step move, and piece is not Cannon
                    elif occupied and vector == vector_sequence[-1] and piece != Cannon:
                        disqualified = False
                        capture = True
                        halt = True
                    # Occupied by opponent piece and is the first-step of a two-step Horse move
                    elif occupied:
                        disqualified = True
                        halt = True

                    # Special Case: Cannon Capture
                    # If halted, and not reached end of board, 
                    # Cannon has encountered a piece it can use as a 'platform'
                    # Check if there is an opponent piece on the axis past the 'platform'
                    
                    if piece == Cannon and not cannon_platform:
                    
                        disqualified = True

                    if piece == Cannon and cannon_platform:
                        disqualified = False
                        

                    if piece == Cannon and occupied:
                        # Cannon platform encountered
                        if not cannon_platform:
                            cannon_platform = True
                            halt = False


                       
                    

                    if disqualified:
                        break

                # 4. Create a move and add to list
                if not disqualified:
                    move = Move((file, rank), (new_file, new_rank), capture)
                    moves.append(move)

                # If the given piece can move any distance along an axis (e.g. Cannon or Rook)
                # the loop should continue until an obstruction is encountered or end of board reached
                should_advance = any_dist

        return moves

    # Given a board state and a single piece location, generate a list of pseudo-legal moves but with move score given
    # @param usermove refers to either self.userthreats or self.aithreats (These two threats are passed to the AI on init and passed to this function as parameters when called by the AI minimax function)
    # @param color refers to which side is playing to determine soldier value
    @staticmethod
    def generate_pseudo_valid_moves_order(board, file, rank, color, usermove):
        """
        Given a board state and a single piece location, generate a list of pseudo-legal moves
        :@param file {int} vertical line on board, range={1..9}
        :@param rank {int} horizontal line on board, range={1..10}

        Static function allowing to generate moves for the potential board states

        :@return moves {[Move]} list of pseudo-legal moves
        """
        
        if color == "w":
            red_side = True
        else:
            red_side = False

        # List of pseudo-legal moves
        moves = []
       

        # Identify piece occupying given location
        unknown_piece = board[(rank-1)*9 + (file-1)] 
        piece = PIECE_MAPPING[unknown_piece.upper()]
        piece_val = piece.get_value(file, rank, red_side)


        # Get the movement specification of the given piece 
        vectors, any_dist, area = piece.get_move_vectors(file, rank, unknown_piece.islower()) 
        
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

            # Whether the last considered move should be disqualified
            disqualified = False
            # Whether the current sequence of move should be stopped
            # e.g. If way obstructed, do not consider the remaining positions
            halt = False

            capture = False
            cannon_platform = False
            should_advance = True
            
            # This loop allows to model moves of any distance along an axis
            while should_advance and not halt:

                # For all pieces, apart for Horse this will run once
                # (Horse has a two-stage move)
                for vector in vector_sequence:

                    # 1. Compute resulting new position
                    new_file += vector[0]
                    new_rank += vector[1]
                    
                    # 2. Check if new location is within bounds
                    if not (min_file <= new_file <= max_file) or not (min_rank <= new_rank <= max_rank):
                        # Outside the bounding area, check next option
                        disqualified = True
                        halt = True
                        break

                    # 3. Check if new location is occupied
                    occupied, friendly = Board.is_occupied(board, new_file, new_rank, unknown_piece)

                    # Occupied by friendly piece
                    if occupied and friendly:
                        disqualified = True
                        halt = True
                    # Occupied by opponent piece, is a single-step move, and piece is not Cannon
                    elif occupied and vector == vector_sequence[-1] and piece != Cannon:
                        disqualified = False
                        capture = True
                        halt = True
                    # Occupied by opponent piece and is the first-step of a two-step Horse move
                    elif occupied:
                        disqualified = True
                        halt = True

                    # Special Case: Cannon Capture
                    # If halted, and not reached end of board, 
                    # Cannon has encountered a piece it can use as a 'platform'
                    # Check if there is an opponent piece on the axis past the 'platform'
                    if piece == Cannon and occupied:
                        # Cannon platform encountered
                        if not cannon_platform:
                            cannon_platform = True
                            halt = False
                        # Enemy piece encountered after platform, can capture
                        elif cannon_platform and not friendly:
                            disqualified = False
                            capture = True
                            halt = True
                    # Cannon cannot move past obstruction, only capture
                    elif piece == Cannon and cannon_platform:
                        disqualified = True

                    if disqualified:
                        break


                # 4. Create a move and add to list

                # Moves that enter the enemy line of fire are given a lower score while moves that avoid enemy line of fire are given a higher score
                
                if not disqualified and capture == False:
                    if (new_file, new_rank) in usermove:
                        move = Move((file, rank), (new_file, new_rank), capture, -1)
                        moves.append(move)
                    else:
                        move = Move((file, rank), (new_file, new_rank), capture, 5)
                        moves.append(move) 
                    
                # Move that capture the enemy high value piece with a low value piece is given a higher score that just normal capturing move   
                elif not disqualified and capture == True:
                    captured_piece = board[(new_rank-1)*9 + (new_file-1)] 
                    captured_piece = PIECE_MAPPING[captured_piece.upper()]
                    captured_val = captured_piece.get_value(file, rank, red_side)
                    diff_val = piece_val - captured_val
                    if (diff_val >= 0):
                        move = Move((file, rank), (new_file, new_rank), capture, 10)
                        moves.append(move)
                    else:
                        move = Move((file, rank), (new_file, new_rank), 0)
                        moves.append(move)


                # If the given piece can move any distance along an axis (e.g. Cannon or Rook)
                # the loop should continue until an obstruction is encountered or end of board reached
                should_advance = any_dist

        

        return moves
    
    # Static Helper Functions Below

   
    @staticmethod
    def is_occupied(board, file, rank, piece):
        occupier = board[(rank-1)*9 + (file-1)]
        if occupier != "+":
            occupied = True
            friendly = occupier.islower() == piece.islower()
        else:
            occupied = False
            friendly = False
        return occupied, friendly

    @staticmethod
    def kings_facing(board):
        # Find kings within palace
        black_king = Board.find_king(board)
        red_king = Board.find_king(board, red_side=True)
        # Check if they are on different files
        if black_king[0] != red_king[0]:
            return False
        else:
            file = black_king[0]
            # Check if there are obstructions on the way
            for rank in range(black_king[1], red_king[1]):
                if board[(rank-1)*9 + (file-1)] != "+":
                    # Obstruction found, kings not facing each other directly
                    return False
        return True
    
    @staticmethod
    def find_king(board, red_side=False):
        # Note: If both king's positions would be stored, this function could potentially be removed

        min_file, max_file = (4,6)
        # Define king's palace
        if red_side:
            min_rank, max_rank = (8,10)
            king = "k"
        else:
            min_rank, max_rank = (1,3)
            king = "K"

        for rank in range(min_rank, max_rank+1):
            for file in range(min_file, max_file+1):
                if board[(rank-1)*9 + (file-1)] == king:
                    return file, rank

    @staticmethod 
    def is_check(board, red_side=False):
        # Find given player's king
        kings_position = Board.find_king(board, red_side)

        # Generate all the moves for the opponent player only
        for rank in range(1, 10+1):
            for file in range(1, 9+1):
                piece = board[(rank-1)*9 + (file-1)]
                if (not red_side and piece.islower()) or (red_side and piece.isupper()):
                    moves = Board.generate_pseudo_valid_moves(board, file, rank)
                    # If any move results in king's current position then king is at check
                    if any(map(lambda move: move.target == kings_position, moves)):
                        return True

        return False
    
    
            




        








