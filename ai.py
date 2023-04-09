import math
from time import time

from board import Board, PIECE_MAPPING

"""
class AI
(Should be renamed to a cool name)

@:var side {char} side the AI plays on; b for black side, w for white side
@:var board: {Board} reference to current Board object
@:var positions: {[(int, int)]} current positions of the pieces of the AI

TODO: Implement Evaluation Heuristic Function
TODO: Implement Vanilla Minimax
TODO: Make AI Use Minimax to Make a Move
TODO: Implement Ordering Heuristic
TODO: Implement Alpha-Beta Pruning
TODO: Perform Reinforcement Learning to find Optimal Weightage for Evaluation Heuristics
"""

BLACK_START_POSITIONS = [(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (2,3), (8,3), (1,4), (3,4), (5,4), (7,4), (9,4)]
WHITE_START_POSITIONS = [(1,10), (2,10), (3,10), (4,10), (5,10), (6,10), (7,10), (8,10), (9,10), (2,8), (8,8), (1,7), (3,7), (5,7), (7,7), (9,7)]

# Minimax configuration
MAX = 1
MIN = -1
MAX_DEPTH = 4

# Weights for evaluation heurstics
# [material, mobility, threats]
# currently initialised to be of equal importance
# TODO: Perform Reinforcement Learning to find optimum weightage
WEIGHTS = [1, 1, 1]

class AI:

    def __init__(self, side, board, usermove, aimove):
        self.side = side
        if side == "b":
            self.positions = set(BLACK_START_POSITIONS)
        else:
            self.positions = set(WHITE_START_POSITIONS)
        self.board = board
        self.usermove = usermove
        self.aimove = aimove

    def perform_move(self):
        """
        Make AI perform a move based on current state of the board

        :@return best_move {Move} the most optimum move
        :@return best_score {float} the score of the most optimum move
        :@return time_taken {float} the time taken to compute a move in seconds
        """
        # Measure time taken to compute best move
        start_time = time()
        self.moves_considered = 0

        # Call minimax to find best move
        best_move, best_score = self.minimax(self.board.state, MAX_DEPTH, 1, -math.inf, math.inf, MAX)
        
        # Update piece positions
        self.update_positions(best_move.start, best_move.target)

        end_time = time()
        time_taken = end_time - start_time

        return best_move, best_score, time_taken

    

    def minimax(self, board, max_depth, depth, alpha, beta, turn):
        """
        Implementation of the vanilla minimax algorithm

        TODO: Implement Alpha-Beta Pruning (see below)
        TODO: Implement ordering to optimise Alpha-Beta Pruning (see below)
        TODO: Optional extension: Implement multi-threading

        :@param board {[char]} the hypothetical state of the board
        :@param max_depth {int} maximum depth of recursion in the game tree
        :@param depth (int) current depth in the game tree
        :@param turn (int) specifies MAX or MIN at the current level

        :@return best_move {Move} the most optimum move
        :@return best_score {float} the score of the most optimum move
        """

        # For each position, find available moves
        moves = []
        for rank in range(1, 10+1):
            for file in range(1, 9+1):
                piece = board[(rank-1)*9 + (file-1)]
                # No piece at this positon
                if piece == "+":
                    continue
                # AI's piece and AI's turn
                elif self.is_mine(piece) and turn == MAX:
                    moves += Board.generate_pseudo_valid_moves_order(board, file, rank, self.side, self.usermove)
                # Opponent's piece and Opponent's turn
                elif not self.is_mine(piece) and turn == MIN:
                    if self.side == 'w':
                        side = 'b'
                    else: side = 'w'

                    moves += Board.generate_pseudo_valid_moves_order(board, file, rank, side, self.aithreats)

        # Keep track of best seen move
        best_move = None
        if turn == MAX: best_score = -math.inf
        else: best_score = math.inf

        # TODO: Order the moves list here and implement alpha-beta in loop below

        

        for move in moves:
            simulated_board = Board.simulate_move(board, move)
            self.moves_considered += 1

            # If maximum depth reached, evaluate resulting positions
            if depth == max_depth:
                score = self.evaluate(simulated_board)
            # Else continue to recursively call minimax
            else:
                if turn == MAX: new_turn = MIN
                else: new_turn = MAX

                _, score = self.minimax(simulated_board, max_depth, depth+1, alpha, beta, new_turn)

            # Update best move
            if (turn == MAX and score > best_score): 
                best_score = score
                best_move = move
                alpha = max(alpha, best_score)
                if (beta <= alpha):
                    break

            elif (turn == MIN and score < best_score):
                best_score = score
                best_move = move
                beta = min(beta, best_score)
                if (beta <= alpha):
                    break

        return best_move, best_score
    
    def order_moves(self, moves):



        return 0
    
    def update_positions(self, old_position, new_position=None):
        """
        Update the AI's list of current piece positions

        :@param old_position {(int, int)} old position of the piece
        :@param new_position {(int, int)} new position of the piece, if None then that piece has been captured and has no new position
        """
        self.positions.remove(old_position)
        if new_position:
            self.positions.add(new_position)

    def evaluate(self, curr_board):
        """
        Given the hypothetical state of the board and hypothetical positions of AI's pieces in the current state of the game tree, return a numerical evaluation score.

        :@param curr_board {[char]} hypothetical state of the board; for performance purposes this is NOT the class Board
        :@param curr_positions {(int, int)} hypothetical positions of AI's pieces
        """

        # 1. Material Heuristic - Piece Value and Count
        material = self.material_heuristic(curr_board)
        # print("MATERIAL = ", material_heuristic)

        # 2. Mobility Heuristic - Number of Available Moves
        # 3. Threat Heuristic - Number of Pieces Player's Can Threat
        mobility, threats = self.mobility_and_threat_heuristic(curr_board)
        
        heuristics = [material, mobility, threats]
        final_score = sum([heuristic * weight for heuristic, weight in zip(heuristics, WEIGHTS)])

        return final_score
    
    def material_heuristic(self, curr_board):
        """
        Given the hypothetical state of the board in the current state of the game tree, return the difference in the material value of the pieces AI holds and opponent holds.

        :@param curr_board {[char]} hypothetical state of the board; for performance purposes this is NOT the class Board

        :@return score {float} the material heuristic; the greater the better for AI
        """
        ai_score = 0
        opponent_score = 0

        if self.side == "w":
            red_side = True
        else:
            red_side = False

        for rank in range(1, 10+1):
            for file in range(1, 9+1):
                piece = curr_board[(rank-1)*9 + (file-1)]

                # No piece at this positon
                if piece == "+":
                    continue
                # AI's piece
                elif self.is_mine(piece):
                    piece_type = PIECE_MAPPING[piece.upper()]
                    ai_score += piece_type.get_value(file, rank, red_side)
                # Opponent's piece
                else:
                    piece_type = PIECE_MAPPING[piece.upper()]
                    opponent_score += piece_type.get_value(file, rank, not red_side)

        difference = ai_score - opponent_score
        return difference

    def is_mine(self, piece):
        if self.side == "b" and piece.isupper():
            return True
        elif self.side == "w" and piece.islower():
            return True
        else:
            return False

    def mobility_and_threat_heuristic(self, curr_board):
        """
        Given the hypothetical state of the boardin the current state of the game tree, return the difference in the number of available moves between the AI and the player (mobility heuristic); and difference in the number of threats a player can make (threat heuristic).

        The assumption is that moves of every piece or are of equal worth.

        :@param curr_board {[char]} hypothetical state of the board; for performance purposes this is NOT the class Board

        :@return score {float} the mobility heuristic; the greater the better for AI
        :@return score {float} the threat heuristic; the greater the better for AI
        """

        ai_mobility = 0
        opponent_mobility = 0

        ai_threats = 0
        opponent_threats = 0

        for rank in range(1, 10+1):
            for file in range(1, 9+1):
                # Check if position occupied
                piece = curr_board[(rank-1)*9 + (file-1)]
                if piece == "+":
                    continue
                
                # Generate the moves for this position
                moves = Board.generate_pseudo_valid_moves(curr_board, file, rank)

                # Check the number of threats - capture moves
                threats = len(list(filter(lambda move: move.capture, moves)))

                # AI's piece
                if self.is_mine(piece):
                    ai_mobility += len(moves)
                    ai_threats += threats
                # Opponent's piece
                else:
                    opponent_mobility += len(moves)
                    opponent_threats += threats

        mobility_difference = ai_mobility - opponent_mobility
        threat_difference = ai_threats - opponent_threats
        return mobility_difference, threat_difference


