"""
class Move - Essentially a struct for storing move data

@:var start {(int, int)} starting position of piece
@:var target: {(int, int)} target square that piece can move to
@:var capture: {bool} is it a capture move
"""


class Move:
    def __init__(self, start, target, capture=False):
        self.target = target
        self.start = start
        self.capture = capture

    def __str__(self):
        return "Move from " + str(self.start) + " to " + str(self.target)