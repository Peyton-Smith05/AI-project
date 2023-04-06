import random
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

class AI:

    def __init__(self, side, board):
        self.side = side
        if side == "b":
            self.positions = set(BLACK_START_POSITIONS)
        else:
            self.positions = set(WHITE_START_POSITIONS)
        self.board = board

    def perform_move(self):
        """
        Make AI perform a move based on current state of the board

        :@return move {Move} the most optimum move
        """
        # TOOD: Call minimax when implemented

        # Temporary random move
        # 1. Choose piece at random
        piece = random.choice(list(self.positions))
        # 2. Choose a random move for that piece
        moves = self.board.generateValidMoves(piece[0], piece[1])
        move = random.choice(moves)
        # 3. Update positions after move
        self.update_positions(move.start, move.target)
        return move

    def update_positions(self, old_position, new_position=None):
        """
        Update the AI's list of current piece positions

        :@param old_position {(int, int)} old position of the piece
        :@param new_position {(int, int)} new position of the piece, if None then that piece has been captured and has no new position
        """
        self.positions.remove(old_position)
        if new_position:
            self.positions.add(new_position)

    def evaluate(self, curr_board, curr_positions):
        """
        Given the hypothetical state of the board and hypothetical positions of AI's pieces in the current state of the game tree, return a numerical evaluation score.

        :@param curr_board {[char]} hypothetical state of the board; for performance purposes this is NOT the class Board
        :@param curr_positions {(int, int)} hypothetical positions of AI's pieces
        """

        # 1. Material Heuristic - Piece Value and Count
        material_heuristic = self.material_heuristic(curr_board, curr_positions)
        print("MATERIAL = ", material_heuristic)

        # 2. Mobility Heuristic - Number of Available Moves
        # 3. Threat Heuristic - Number of Pieces Player's Can Threat
        mobility_heuristic, threat_heuristic = self.mobility_and_threat_heuristic(curr_board, curr_positions)
        print("MOBILITY = ", mobility_heuristic)
        print("THREATS = ", threat_heuristic)

        # 4. King Safety Heuristic
        # self.king_safety_heristic(curr_board, curr_positions)

        return material_heuristic + mobility_heuristic + threat_heuristic

    
    def material_heuristic(self, curr_board, curr_positions):
        """
        Given the hypothetical state of the board and hypothetical positions of AI's pieces in the current state of the game tree, return the difference in the material value of the pieces AI holds and opponent holds.

        :@param curr_board {[char]} hypothetical state of the board; for performance purposes this is NOT the class Board
        :@param curr_positions {(int, int)} hypothetical positions of AI's pieces

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

    def mobility_and_threat_heuristic(self, curr_board, curr_positions):
        """
        Given the hypothetical state of the board and hypothetical positions of AI's pieces in the current state of the game tree, return the difference in the number of available moves between the AI and the player (mobility heuristic); and difference in the number of threats a player can make (threat heuristic).

        The assumption is that moves of every piece or are of equal worth.

        :@param curr_board {[char]} hypothetical state of the board; for performance purposes this is NOT the class Board
        :@param curr_positions {(int, int)} hypothetical positions of AI's pieces

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
                if curr_board[(rank-1)*9 + (file-1)] == "+":
                    continue
                
                # Generate the moves for this position
                moves = Board.generate_pseudo_valid_moves(curr_board, file, rank)

                # Check the number of threats - capture moves
                threats = len(list(filter(lambda move: move.capture, moves)))

                # AI's piece
                if (file, rank) in curr_positions:
                    ai_mobility += len(moves)
                    ai_threats += threats
                # Opponent's piece
                else:
                    opponent_mobility += len(moves)
                    opponent_threats += threats

        mobility_difference = ai_mobility - opponent_mobility
        threat_difference = ai_threats - opponent_threats
        return mobility_difference, threat_difference


