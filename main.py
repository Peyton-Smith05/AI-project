# Example file showing a basic pygame "game loop"

# This is a sample Python script.

import board
import random 
from move import Move

from os import system, name

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

    new_move = Move(start, target)
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

while True:

    print(board)
    

    # TODO: For now the game is playable by two humans only
    # if board.turn == human_color:
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
        move = getMoveFromString(start_str, target_str)

        clear_screen()
        board.updateBoardFromMove(move)

    else:
        # TODO:
            # Call generate computer moves

        computer_move = board.generateComputerMove()
        file = computer_move[0]
        rank = computer_move[1]
        computer_move = str(computer_move)
        computer_move = computer_move.replace('[', '')
        computer_move = computer_move.replace(']', '')
        computer_move = computer_move.replace(',', '')
        computer_move = str(computer_move)
        moves = board.generateValidMoves(int(file), int(rank))

        target_str_temp = random.choice(moves)
        print (target_str_temp)
        target_str = input('Please move: ')
        
        
        move = getMoveFromString(computer_move, target_str)
        clear_screen()
        board.updateBoardFromMove(move)

            # Call evaluate moves
            # Call pick best move
            # Call updateBoardFromMove
        continue



