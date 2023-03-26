import pygame
import board
import move

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
    "K": "images/general_w.png", "k": "images/general_b.png",
    "A": "images/advisor_w.png", "a": "images/advisor_b.png",
    "H": "images/horse_w.png", "h": "images/horse_b.png",
    "E": "images/elephant_w.png", "e": "images/elephant_b.png",
    "R": "images/chariot_w.png", "r": "images/chariot_b.png",
    "C": "images/canon_w.png", "c": "images/canon_b.png",
    "P": "images/pawn_w.png", "p": "images/pawn_b.png"
}


class Piece(pygame.sprite.Sprite):
    def __init__(self, image_file, coordinate):
        super(Piece, self).__init__()
        self.surf = pygame.image.load(image_file).convert()
        self.surf = pygame.transform.scale(self.surf, (50, 50))
        self.surf.set_colorkey(BACKGROUND_COLOR)
        self.rect = self.surf.get_rect(
            center=(
                coordinate
            )
        )


def initializePiecesFromBoard(board: board.Board):
    piece_lst = []
    for i in range(len(board.state)):
        if board.state[i] == '+':
            continue
        else:
            new_piece = Piece(PATH_DICT[board.state[i]], COORDINATE_MAP[i])
            piece_lst.append(new_piece)
    return piece_lst


STARTING_STATE_FEN = 'rheakaehr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RHEAKAEHR w - - 0 1'

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

background = pygame.image.load('images/board.png')

screen.fill(BACKGROUND_COLOR)
screen.blit(background, (0, 0))

white_pieces = pygame.sprite.Group()
black_pieces = pygame.sprite.Group()
all_pieces = pygame.sprite.Group()

board = board.Board(STARTING_STATE_FEN, 'b')

piece_lst = initializePiecesFromBoard(board)

for piece in piece_lst:
    all_pieces.add(piece)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            rect = pygame.rect(mouse, (20, 20))
            for piece in all_pieces:
                if pygame.sprite.collide_rect(rect, piece.rect):
                    piece.rect = piece.surf.get_rect(center=mouse)


    # fill the screen with a color to wipe away anything from last frame

    # RENDER YOUR GAME HERE
    # Draw all sprites
    for entity in all_pieces:
        screen.blit(entity.surf, entity.rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()