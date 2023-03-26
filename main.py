# Example file showing a basic pygame "game loop"

# This is a sample Python script.

import board
import move

STARTING_STATE_FEN = 'rheakaehr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RHEAKAEHR w - - 0 1'


# Helper function
def getMoveFromString(start, target):

    # Changing string to integer pos
    start = start.split(" ")
    target = target.split(" ")
    start_x, start_y = int(start[0]), int(start[1])
    target_x, target_y = int(target[0]), int(target[1])

    start = ((start_y - 1) * 9) + (start_x - 1)
    target = ((target_y - 1) * 9) + (target_x - 1)

    new_move = move.Move(start, target)
    return new_move


computer_color = ''

human_color = input("Playing as w or b? ")

if human_color == 'w':
    computer_color = 'b'
else:
    computer_color = 'w'

board = board.Board(STARTING_STATE_FEN, computer_color)

while True:

    print(board)

    if board.turn == human_color:
        start_str = input('Input piece square (Notation is File Rank of piece ex. 2 3): ')
        target_str = input('Input target square by same notation: ')
        move = getMoveFromString(start_str, target_str)
        board.updateBoardFromMove(move)
    else:
        # TODO:
            # Call generate computer moves
            # Call evaluate moves
            # Call pick best move
            # Call updateBoardFromMove
        continue



