import random
from board import Board

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
