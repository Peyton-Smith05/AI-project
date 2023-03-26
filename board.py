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

"""

@:var state {array[90] of char} contains current state of board
@:var turn {char} w | b
@:var king_pos {int} integer position of the turn of current players king within state
                     (this will be needed for determining legal moves)
@:var half_moves {int} number of half moves since last capture. If == 60 then game ends in draw,
                       increments after white or black move
@:var full_moves {int} number of full moves

@:func __init__(self, fen) default constructor, calls helper function generateStringFromFen()
@:func generateStringFromFen(string fen) 
@:func generateValidMoves(1darray board
@:func evaluateBoardPos()

"""


class Board:
    """
    Constructor from fun
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
