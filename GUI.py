import numpy as np
import pygame

import logic

# load images
bg = pygame.image.load("assets\\board.png")

white_img = [pygame.image.load("assets\\pieces\\PawnW.png"),
             pygame.image.load("assets\\pieces\\RookW.png"),
             pygame.image.load("assets\\pieces\\KnightW.png"),
             pygame.image.load("assets\\pieces\\BishopW.png"),
             pygame.image.load("assets\\pieces\\QueenW.png"),
             pygame.image.load("assets\\pieces\\KingW.png"),
             pygame.image.load("assets\\pieces\\RookW.png"),
             pygame.image.load("assets\\pieces\\KingW.png")
             ]

black_img = [pygame.image.load("assets\\pieces\\PawnB.png"),
             pygame.image.load("assets\\pieces\\RookB.png"),
             pygame.image.load("assets\\pieces\\KnightB.png"),
             pygame.image.load("assets\\pieces\\BishopB.png"),
             pygame.image.load("assets\\pieces\\QueenB.png"),
             pygame.image.load("assets\\pieces\\KingB.png"),
             pygame.image.load("assets\\pieces\\RookB.png"),
             pygame.image.load("assets\\pieces\\KingB.png")
             ]

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


def blit_pieces(board: np.ndarray):
    start_x = 82
    start_y = 84
    piece_size = 80

    pieces = np.nonzero(np.reshape(board[:, :, 1], (8, 8)))
    for y, x in zip(pieces[0], pieces[1]):
        piece = board[y, x]
        piece_y = start_y+(piece_size*y)
        piece_x = start_x+(piece_size*x)
        # white piece
        if piece[0] == 1:
            display.blit(white_img[piece[1]-1], (piece_x, piece_y))
        # black piece
        else:
            display.blit(black_img[piece[1]-1], (piece_x, piece_y))


def get_moves(board, turn, check):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    curr_pos = (((mouse_y-84)//80), ((mouse_x-82)//80))
    if curr_pos[0] < 8 and curr_pos[1] < 8:
        if turn == board[curr_pos[0], curr_pos[1], 0]:
            moves = logic.return_possible_moves(board, curr_pos, turn)
            if check:
                moves = logic.block_check_moves(board, curr_pos, moves, turn)
            return moves, curr_pos


def blit_possible_moves(shown_moves):
    for y, x in list(shown_moves.values())[0]:
        x_cor = 42+(x+1)*80
        y_cor = 45+((y+1)*80)
        pygame.draw.circle(display, (138, 85, 85), (x_cor, y_cor), 16)


def update_position(board, shown_moves, turn):
    # if mouse is clicked over legal move piece there, else return false
    mouse_x, mouse_y = pygame.mouse.get_pos()
    wanted_pos = (((mouse_y - 84) // 80), ((mouse_x - 82) // 80))
    if shown_moves:
        if wanted_pos in list(shown_moves.values())[0]:
            last_pos = list(shown_moves.keys())[0]
            return logic.update_pos(board, last_pos, wanted_pos, turn)
    return None


def blit_gui(board: np.ndarray, shown_moves):
    display.blit(bg, (0, 0))
    blit_pieces(board)
    if shown_moves:
        blit_possible_moves(shown_moves)
