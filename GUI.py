import pygame
import logic

pygame.init()

# load images
bg = pygame.image.load("assets\\board.png")

white_img = [pygame.image.load("assets\\pieces\\PawnW.png"),
             pygame.image.load("assets\\pieces\\RookW.png"),
             pygame.image.load("assets\\pieces\\KnightW.png"),
             pygame.image.load("assets\\pieces\\BishopW.png"),
             pygame.image.load("assets\\pieces\\QueenW.png"),
             pygame.image.load("assets\\pieces\\KingW.png")]

black_img = [pygame.image.load("assets\\pieces\\PawnB.png"),
             pygame.image.load("assets\\pieces\\RookB.png"),
             pygame.image.load("assets\\pieces\\KnightB.png"),
             pygame.image.load("assets\\pieces\\BishopB.png"),
             pygame.image.load("assets\\pieces\\QueenB.png"),
             pygame.image.load("assets\\pieces\\KingB.png")]

##################################################################################
board = pygame.display.set_mode((1200, 800))
active_pieces = []
# create grid (y,x )


def move_pieces(piece, position):
    pass


def create_pices(piece, color, restart_position):
    global active_pieces
    # check color than blit images of coresponding pieces at cordinates of grid
    x, y = restart_position
    if color == 0:  # white
        board.blit(white_img[piece], (create_grid()[y][x]))
    else:  # black
        board.blit(black_img[piece], (create_grid()[y][x]))


def create_grid():
    # grid start 82, 86 size 80*80
    start_x = 82
    start_y = 84
    pcs_size = 80
    grid = [
        [[], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], []],

    ]
    for y in range(8):
        for x in range(8):  # fill list with coridnates of grid
            grid[y][x] = ((start_x + (pcs_size*x), start_y+(pcs_size*y)))
    return grid


def display_update():
    board.blit(bg, (0, 0))
    create_grid()
    logic.restart_pieces()
    pygame.display.update()
