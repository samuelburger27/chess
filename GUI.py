import numpy as np
import pygame
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

white_convert_img = [pygame.image.load("assets\\pawn_transformation_UI\\black_basic.png"),
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
display = pygame.display.set_mode((1200, 800))
dont_show_this_piece = None
show_convert_UI = False


def piece_follow_mouse(piece):
    global dont_show_this_piece
    x, y = pygame.mouse.get_pos()
    dont_show_this_piece = piece.id
    if piece.color == 0:  # white
        display.blit(white_img[piece.piece], (x - 40, y - 40))
    else:  # black
        display.blit(black_img[piece.piece], (x - 40, y - 40))


def blit_pieces(board: np.ndarray):
    start_x = 86
    start_y = 82
    piece_size = 80

    # remove axis 2 so we don't have duplicates [0, 0]-> 0, [1, 5]-> 6
    pieces = np.nonzero(np.sum(board, axis=2))
    for y, x in zip(pieces[0], pieces[1]):
        piece = board[y, x]
        piece_y = start_y+(piece_size*y)
        piece_x = start_x+(piece_size*x)
        # white piece
        if piece[0] < 30:
            display.blit(white_img[piece[1]-1], (piece_x, piece_y))
        # black piece
        else:
            display.blit(black_img[piece[1]-1], (piece_x, piece_y))


def blit_gui(board: np.ndarray):
    display.blit(bg, (0, 0))
    blit_pieces(board)
