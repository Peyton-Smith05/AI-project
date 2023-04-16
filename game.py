import math

import pygame
import board
import move
import piece
import ai

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 720
BACKGROUND_COLOR = (241, 203, 157)

COORDINATE_MAP = [
    (36, 32), (107, 32), (178, 32), (249, 32), (320, 32), (391, 32), (462, 32), (533, 32), (604, 32),
    (36, 105), (107, 105), (178, 105), (249, 105), (320, 105), (391, 105), (462, 105), (533, 105), (604, 105),
    (36, 178), (107, 178), (178, 178), (249, 178), (320, 178), (391, 178), (462, 178), (533, 178), (604, 178),
    (36, 251), (107, 251), (178, 251), (249, 251), (320, 251), (391, 251), (462, 251), (533, 251), (604, 251),
    (36, 324), (107, 324), (178, 324), (249, 324), (320, 324), (391, 324), (462, 324), (533, 324), (604, 324),
    (36, 400), (107, 400), (178, 400), (249, 400), (320, 400), (391, 400), (462, 400), (533, 400), (604, 400),
    (36, 472), (107, 472), (178, 472), (249, 472), (320, 472), (391, 472), (462, 472), (533, 472), (604, 472),
    (36, 544), (107, 544), (178, 544), (249, 544), (320, 544), (391, 544), (462, 544), (533, 544), (604, 544),
    (36, 616), (107, 616), (178, 616), (249, 616), (320, 616), (391, 616), (462, 616), (533, 616), (604, 616),
    (36, 690), (107, 690), (178, 690), (249, 690), (320, 690), (391, 690), (462, 690), (533, 690), (604, 690),
]

PATH_DICT = {
    "k": "images/general_w.png", "K": "images/general_b.png",
    "a": "images/advisor_w.png", "A": "images/advisor_b.png",
    "h": "images/horse_w.png", "H": "images/horse_b.png",
    "e": "images/elephant_w.png", "E": "images/elephant_b.png",
    "r": "images/chariot_w.png", "R": "images/chariot_b.png",
    "c": "images/canon_w.png", "C": "images/canon_b.png",
    "p": "images/pawn_w.png", "P": "images/pawn_b.png"
}

AI_MOVE = pygame.USEREVENT + 1


class Piece(pygame.sprite.Sprite):
    def __init__(self, image_file, coordinate, value):
        super(Piece, self).__init__()
        self.color = 'w' if value.islower() else 'b'
        self.image = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = coordinate

    def update(self, mouse_pos):
        self.rect.center = mouse_pos


class Button(pygame.sprite.Sprite):
    def __init__(self, image_file, coordinate, color):
        super(Button, self).__init__()
        self.color = color
        self.image = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 50))
        self.rect = self.image.get_rect()
        self.rect.center = coordinate


class Dot(pygame.sprite.Sprite):
    def __init__(self, coordinate, move):
        super(Dot, self).__init__()
        self.image = pygame.image.load('images/red_dot.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.center = coordinate
        self.move = move


def initializePiecesFromBoard(b: board.Board):
    p_lst = []
    for i in range(len(b.state)):
        if b.state[i] == '+':
            continue
        else:
            new_piece = Piece(PATH_DICT[b.state[i]], COORDINATE_MAP[i], b.state[i])
            p_lst.append(new_piece)
    return p_lst


def getMinDistance(mouse_pos):
    minimum = 10000
    point = 0
    for x in range(len(COORDINATE_MAP)):
        val = math.dist(COORDINATE_MAP[x], mouse_pos)
        if val < minimum:
            minimum = val
            point = COORDINATE_MAP[x]
    return point


STARTING_STATE_FEN = 'rheakaehr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RHEAKAEHR w - - 0 1'

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

background = pygame.image.load('images/board.png')

screen.fill(BACKGROUND_COLOR)

# Starting screen
starting_screen = True

player_color = 0

starting_buttons = pygame.sprite.Group()

# Get two buttons and blit text onto screen
black_btn = Button('images/black_button.png', (500, 400), 'b')
white_btn = Button('images/red_button.png', (500, 320), 'w')

starting_buttons.add(black_btn)
starting_buttons.add(white_btn)

# Getting text
intro_text_pos = (420, 250)
intro_text = 'Choose a color:'

font = pygame.font.SysFont("timesnewroman", 26)

text_surface = font.render(intro_text, True, (0, 0, 0))

while starting_screen:
    clicked_button = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            for button in starting_buttons:
                if button.rect.collidepoint(event.pos):
                    clicked_button = button

    screen.fill(BACKGROUND_COLOR)
    starting_buttons.draw(screen)
    screen.blit(text_surface, intro_text_pos)
    pygame.display.flip()

    if not clicked_button:
        continue
    elif clicked_button.color == 'w':
        player_color = 'w'
        starting_screen = False
    elif clicked_button.color == 'b':
        player_color = 'b'
        starting_screen = False

if player_color == 'w':
    computer_color = 'b'
else:
    computer_color = 'w'
# Group set up

font = pygame.font.SysFont("timesnewroman", 15)

dumbo_image = pygame.image.load('images/dumbo.png')
dumbo_image = pygame.transform.scale(dumbo_image, (150, 150))
dumbo_pos = (650, 50) if computer_color == 'b' else (650, 500)
valid_move_dots = pygame.sprite.Group()
game_pieces = pygame.sprite.Group()

# Initializers for all
board = board.Board(STARTING_STATE_FEN, computer_color)
board_userthreats = board.userthreats
board_aithreats = board.aithreats
ai = ai.AI(computer_color, board, board_userthreats, board_aithreats, 4)

# Text Initialization
turn_text_pos = (750, 375)
move_text_pos = (800, 50) if computer_color == 'b' else (800, 500)
score_text_pos = (800, 75) if computer_color == 'b' else (800, 525)
time_text_pos = (800, 100) if computer_color == 'b' else (800, 550)
comment_pos = (650, 225) if computer_color == 'b' else (650, 425)

time_text = 'Time: 0.0'
move_text = '(0, 0)'
score_text = 'Score: 0'
turn_text = 'Turn: ' + board.turn

time_text_surface = font.render(time_text, True, (0, 0, 0))
move_text_surface = font.render(move_text, True, (0, 0, 0))
score_text_surface = font.render(score_text, True, (0, 0, 0))
turn_text_surface = font.render(turn_text, True, (0, 0, 0))
comment_surface = font.render('Lets begin!', True, (0, 0, 0))

piece_lst = initializePiecesFromBoard(board)

for piece in piece_lst:
    game_pieces.add(piece)

selected_piece = None

ai_move_event = pygame.event.Event(AI_MOVE)
pygame.event.post(ai_move_event)

screen.fill(BACKGROUND_COLOR)
screen.blit(background, (0, 0))
screen.blit(dumbo_image, dumbo_pos)

game_pieces.draw(screen)
valid_move_dots.draw(screen)

screen.blit(move_text_surface, move_text_pos)
screen.blit(score_text_surface, score_text_pos)
screen.blit(turn_text_surface, turn_text_pos)
screen.blit(time_text_surface, time_text_pos)
screen.blit(comment_surface, comment_pos)

pygame.display.flip()
ai_time_rec = []
num_moves = 0

move_data = []

end = False

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            total_time = sum(ai_time_rec)
            av_time = total_time / len(ai_time_rec)

            text_file = open("game_stats.txt", 'w')
            text_file.write('Number of Moves: \t' + str(len(ai_time_rec)) + '\n')
            text_file.write('Total Time: \t' + str(total_time) + '\n')
            text_file.write('Time/Move: \t' + str(av_time) + '\n')

            text_file.write('List of moves: \n')
            for move in move_data:
                text_file.write(move)

            running = False
        elif event.type == pygame.MOUSEBUTTONUP and player_color == board.turn:

            """
            On mouse button up check what was selected
            if it was a piece, check if it is the right color
                if it is the right color
                    generate valid moves for that piece
                    clear valid_moves_dot from the old one
                    update valid_moves_dot with new valid moves
            else if it is valid move dot
                get the move 
                update the board state from the move
                clear piece sprite list
                recreate sprite list 
                clear valid_moves_dot
                
            """
            selected_piece = None
            for move in valid_move_dots:
                if move.rect.collidepoint(event.pos):
                    selected_piece = move
            if selected_piece is not None:
                board.updateBoardFromMove(selected_piece.move)
                turn_text = 'Turn:' + board.turn
                turn_text_surface = font.render(turn_text, True, (0, 0, 0))
                game_pieces.empty()

                piece_lst = initializePiecesFromBoard(board)

                for piece in piece_lst:
                    game_pieces.add(piece)
                valid_move_dots.empty()
                ai_move_event = pygame.event.Event(AI_MOVE)
                pygame.event.post(ai_move_event)

                end, player = board.checkForEndGame()

            else:
                for piece in game_pieces:
                    if piece.rect.collidepoint(event.pos) and piece.color == player_color:
                        selected_piece = piece
                if selected_piece is not None:
                    # get file and rank of the piece
                    ind = COORDINATE_MAP.index(selected_piece.rect.center)
                    moves = board.generateValidMoves((ind % 9) + 1, (ind // 9) + 1)
                    valid_move_dots.empty()
                    for move in moves:
                        new_dot = Dot(COORDINATE_MAP[((move.target[1] - 1) * 9) + (move.target[0] - 1)], move)
                        valid_move_dots.add(new_dot)


        elif event.type == AI_MOVE and board.turn == computer_color:
            """
            Display AI thinking
            calculate the move
            get the number of possibilities and the time it takes to calculate
            update the text for that so that it is blit in the next loop
            update the board state
            recreate piece sprites
            
            """
            comment_surface = font.render('Interesting... Let me think about this', True, (0, 0, 0))
            screen.blit(comment_surface, (comment_pos[0], comment_pos[1] + 20))
            pygame.display.flip()
            move, score, time = ai.perform_move()
            board.updateBoardFromMove(move)
            turn_text = 'Turn: ' + board.turn
            turn_text_surface = font.render(turn_text, True, (0, 0, 0))
            game_pieces.empty()
            ai_time_rec.append(time)
            num_moves += 1

            move_str = str(move) + '\nScore: \t' + str(score) + '\n'
            move_data.append(move_str)

            piece_lst = initializePiecesFromBoard(board)

            for piece in piece_lst:
                game_pieces.add(piece)
            valid_move_dots.empty()

            comment_surface = font.render('Take that!', True, (0, 0, 0))
            screen.blit(comment_surface, comment_pos)

            time_text = 'Time taken: ' + str(time)
            move_text = str(move)
            score_text = 'Score: ' + str(score)
            turn_text = 'Turn: ' + board.turn
            time_text_surface = font.render(time_text, True, (0, 0, 0))
            move_text_surface = font.render(move_text, True, (0, 0, 0))
            score_text_surface = font.render(score_text, True, (0, 0, 0))
            turn_text_surface = font.render(turn_text, True, (0, 0, 0))

            end, player = board.checkForEndGame()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BACKGROUND_COLOR)
    screen.blit(background, (0, 0))
    screen.blit(dumbo_image, dumbo_pos)
    screen.blit(comment_surface, comment_pos)

    # RENDER YOUR GAME HERE
    # Draw all sprites

    game_pieces.draw(screen)
    valid_move_dots.draw(screen)

    
    if end:
        total_time = sum(ai_time_rec)
        av_time = total_time / len(ai_time_rec)

        text_file = open("game_stats.txt", 'w')
        text_file.write('Number of Moves: \t' + str(len(ai_time_rec)) + '\n')
        text_file.write('Total Time: \t' + str(total_time) + '\n')
        text_file.write('Time/Move: \t' + str(av_time) + '\n')

        text_file.write('List of moves: \n')
        for move in move_data:
            text_file.write(move)

        break

    screen.blit(move_text_surface, move_text_pos)
    screen.blit(score_text_surface, score_text_pos)
    screen.blit(turn_text_surface, turn_text_pos)
    screen.blit(time_text_surface, time_text_pos)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
