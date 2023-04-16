from board import Board
import random 
from move import Move
from ai import AI#
from RL import RL

import os
from os import system, name
import json

STARTING_STATE_FEN = 'rheakaehr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RHEAKAEHR w - - 0 1'

def save_dict_to_file(dictionary, filename):
    with open(filename, 'w') as f:
        json.dump(dictionary, f)

def read_dict_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            dictionary = json.load(f)
            print("MODEL LOADED")
    else:
        print("NO MODEL")
        dictionary = {}
    return dictionary

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


model_dict={}
model_filename="dict.txt"
model_dict=read_dict_from_file(model_filename)
rlmodel=RL(model_dict)
computer_color = ''

#human_color = input("Playing as w or b? ")
human_color = 'b'

if human_color == 'w':
    computer_color = 'b'
else:
    computer_color = 'w'

wins=[]
for game in range(0,4):
    result=0
    board = Board(STARTING_STATE_FEN, computer_color)
    board_userthreats = board.userthreats
    board_aithreats = board.aithreats
    ai = AI(computer_color, board, board_userthreats, board_aithreats,4)
    ai2 = AI(human_color, board, board_userthreats, board_aithreats,2)

    for turn in range (0,70):
        if turn==69:
            wins.append(result)
        if board.turn == human_color:
            #clear_screen()
            end, player = board.checkForEndGame()
            print(board)
            if end == True:
                result=1
                wins.append(result)
                break
            print("AI computing move...")
            move, score, time = ai2.perform_move()
            board.updateBoardFromMove(move)
            #clear_screen()
            print("game num ", game, "round ", turn)
            print("AI: ", move)
            print("Time taken: ", time, " seconds")
            print("Moves combinations considered: ", ai2.moves_considered)
            print("CURR SCORE ", score)

        else:
            #clear_screen()
            end, player = board.checkForEndGame()
            print(board)
            if end == True:
                result=-1
                wins.append(result)
                break
            print("AI computing move...")
            #move, score, time = ai.perform_move()

            move, reward, time= ai.simulate_move()
            best_Q_move, score= rlmodel.compute_move(board,reward,move)
            board.updateBoardFromMove(best_Q_move)
            #clear_screen()
            print("game num ", game, "round ", turn)

            #print("AI: ", best_Q_move)
            print("Time taken: ", time, " seconds")
            print("Moves combinations considered: ", ai.moves_considered)
            print("CURR SCORE ", score)

    model_dict=rlmodel.return_model()
    print(model_dict)
    if os.path.exists(model_filename):
        os.remove(model_filename)
    save_dict_to_file(model_dict,model_filename)

print(wins)
input('Press enter to exit the game')
    
    




