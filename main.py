# Example file showing a basic pygame "game loop"

# This is a sample Python script.

import board
import random 
from move import Move
from ai import AI

from os import system, name

STARTING_STATE_FEN = 'rheakaehr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RHEAKAEHR w - - 0 1'


# Helper function
def getMoveFromString(start, target, board):

    # Changing string to integer pos
    start = start.split(" ")
    target = target.split(" ")
    start_file, start_rank = int(start[0]), int(start[1])
    target_file, target_rank = int(target[0]), int(target[1])

    start = (start_file, start_rank)
    target = (target_file, target_rank)

    # Check if player's move was a capture
    # (will be trivial if player chooses moves from a list)
    if board.state[(target_rank-1)*9 + (target_file-1)] != "+":
        capture = True
    else:
        capture = False

    new_move = Move(start, target, capture)
    return new_move

# Clear screen helper function
def clear_screen():
    # For windows
    if name == 'nt':
        _ = system('cls')
 
    # For macOS and Linux (here, os.name is 'posix')
    else:
        _ = system('clear')


computer_color = ''

human_color = input("Playing as w or b? ")

if human_color == 'w':
    computer_color = 'b'
else:
    computer_color = 'w'

board = board.Board(STARTING_STATE_FEN, computer_color)
ai = AI(computer_color, board)

while True:

    print(board)

    if board.turn == human_color:
        start_str = input('Input piece square (Notation is File Rank of piece ex. 2 3): ')

        file, rank = start_str.split(" ")[:2]
        moves = board.generateValidMoves(int(file), int(rank))

        print("Possible moves:")
        for move in moves:
            print(move)

        print()
        target_str = input('Choose one of the moves by inputting target square by same notation: ')
        
        # TODO: This does not check the target square
        # Maybe the player should choose from the list
        move = getMoveFromString(start_str, target_str, board)
        board.updateBoardFromMove(move)

        # If player has captured AI's piece, notify the AI
        if move.capture:
            ai.update_positions(move.target)

        clear_screen()

    else:
        print("AI computing move...")
        move, time = ai.perform_move()
        board.updateBoardFromMove(move)
        clear_screen()
        print("AI: ", move)
        print("Time taken: ", time, " seconds")

    score = ai.evaluate(board.state)
    print("CURR SCORE ", score)
    
    




