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
dont_show_this_piece = None


def show_posibble_moves(list):
    for tubl in list:
        y, x = grid()[tubl[0]][tubl[1]]
        pygame.draw.rect(board, (255, 0, 0), (x, y, 80, 80), 1)


def piece_follow_mouse(piece):
    global dont_show_this_piece
    x, y = pygame.mouse.get_pos()
    dont_show_this_piece = piece.id
    if piece.color == 0:  # white
        board.blit(white_img[piece.piece], (x-40, y-40))
    else:  # black
        board.blit(black_img[piece.piece], (x-40, y-40))


def blit_piece(piece, color, restart_x, restar_y, id):
    global active_pieces
    # check color than blit images of coresponding pieces at cordinates of grid

    if color == 0 and id != dont_show_this_piece:  # white
        board.blit(white_img[piece], (grid()[restar_y][restart_x]))
    elif color == 1 and id != dont_show_this_piece:  # black
        board.blit(black_img[piece], (grid()[restar_y][restart_x]))


def grid():
    # grid start 82, 86 size 80*80
    start_x = 86
    start_y = 82
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


def show_pieces():
    for pcs in logic.pieces:
        blit_piece(pcs.piece, pcs.color, pcs.curr_x, pcs.curr_y, pcs.id)


def display():
    board.blit(bg, (0, 0))
