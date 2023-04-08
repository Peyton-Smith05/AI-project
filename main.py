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
temp_self = board.usermoves
temp_self2 = board.aimoves
ai = AI(computer_color, board, temp_self, temp_self2)

while True:
    print(board.usermoves)
    print("\n")
    print(board.aimoves)
    if board.turn == human_color:
        move_allowed = False
        while not move_allowed:
            print(board)
            # Ask user for input
            start_str = input('Input piece square (Notation is File Rank of piece ex. 2 3): ')
            file, rank = start_str.split(" ")[:2]
            file = int(file)
            rank = int(rank)

            # Check if position occupied and user's piece
            piece = board.state[(rank-1)*9 + (file-1)]
            if piece == "+" or ai.is_mine(piece):
                clear_screen()
                print("This position is not occupied or is not your piece")
                continue

            # Generate valid moves
            moves = board.generateValidMoves(file, rank)

            # Ask user to choose a different piece if no moves for chosen piece
            if len(moves) == 0:
                clear_screen()
                print("No moves available for this piece")
                continue

            print("Possible moves:")
            for move in moves:
                print(move)

            print()
            target_str = input('Choose one of the moves by inputting target square by same notation or cancel to choose a different piece: ')
            
            # User decided to choose another piece
            if target_str.strip() == "cancel":
                clear_screen()
                continue

            # TODO: This does not check the target square
            # Maybe the player should choose from the list
            move = getMoveFromString(start_str, target_str, board)
            board.updateBoardFromMove(move)

            # If player has captured AI's piece, notify the AI
            if move.capture:
                ai.update_positions(move.target)

            move_allowed = True
            end, player = board.checkForEndGame()
            if end == True:
                break

    else:
        clear_screen()
        end, player = board.checkForEndGame()
        print(board)
        if end == True:
            break
        print("AI computing move...")
        move, score, time = ai.perform_move()
        board.updateBoardFromMove(move)
        clear_screen()
        print("AI: ", move)
        print("Time taken: ", time, " seconds")
        print("Moves combinations considered: ", ai.moves_considered)
        print("CURR SCORE ", score)

input('Press enter to exit the game')
    
    




