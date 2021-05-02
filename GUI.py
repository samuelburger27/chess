import pygame

import logic
from button import button
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

white_conver_img = [pygame.image.load("assets\\pawn_transformation_UI\\black_basic.png"),
                    pygame.image.load(
                        "assets\\pawn_transformation_UI\\black_bishop.png"),
                    pygame.image.load(
                        "assets\\pawn_transformation_UI\\black_knight.png"),
                    pygame.image.load(
                        "assets\\pawn_transformation_UI\\black_queen.png"),
                    pygame.image.load(
                        "assets\\pawn_transformation_UI\\black_rook.png"),
                    ]
black_convert_img = [pygame.image.load("assets\\pawn_transformation_UI\\black_basic.png"),
                     pygame.image.load(
                         "assets\\pawn_transformation_UI\\black_bishop.png"),
                     pygame.image.load(
                         "assets\\pawn_transformation_UI\\black_knight.png"),
                     pygame.image.load(
                         "assets\\pawn_transformation_UI\\black_queen.png"),
                     pygame.image.load(
                         "assets\\pawn_transformation_UI\\black_rook.png"),
                     ]


##################################################################################
board = pygame.display.set_mode((1200, 800))
dont_show_this_piece = None
show_convert_UI = False


def conver_pawn_UI():
    x, y = pygame.mouse.get_pos()
    pos_x = 256
    pos_y = 346
    if logic.current_turn % 2 == 0:  # white color
        used_list = white_conver_img
    else:
        used_list = black_convert_img

    if (x > pos_x and x < pos_x + (285)) and (y > pos_y and y < pos_y+109):
        if x < pos_x + (285/4):
            board.blit(used_list[1], (pos_x, pos_y))
        elif x < pos_x + (285/2):
            board.blit(used_list[2], (pos_x, pos_y))
        elif x < pos_x + ((285/1)*3):
            board.blit(used_list[3], (pos_x, pos_y))
        else:
            board.blit(used_list[4], (pos_x, pos_y))
    else:
        board.blit(used_list[0], (pos_x, pos_y))


def show_posibble_moves(list):
    if len(list) != 0:
        for tubl in list:
            if len(tubl) == 2:
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
