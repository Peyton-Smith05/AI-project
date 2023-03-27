"""
class Move - Essentially a struct for storing move data

@:var start {int} starting position of piece
@:var target: {int} target square that piece can move to
@:var pos_eval: {int(maybe float??)} numerical evaluation of the position it puts the board in
                                        (from perspective of player whose turn it is to move)
"""


class Move:
    def __init__(self, start, target, capture=False):
        self.target = target
        self.start = start
        self.capture = capture
        self.pos_eval = 0

    def __str__(self):
        return "Move from " + str(self.start) + " to " + str(self.target)