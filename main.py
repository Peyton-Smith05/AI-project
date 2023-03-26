# Example file showing a basic pygame "game loop"

# This is a sample Python script.

import board
import move

STARTING_STATE_FEN = 'rheakaehr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RHEAKAEHR w - - 0 1'


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
        move_str = input('Input move (Notation is Rank File of piece, Rank File of Starting Square ex: ')
