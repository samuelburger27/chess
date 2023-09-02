import time

import numpy as np
import pygame

import logic

pygame.init()
# load images
bg = pygame.image.load("assets/board.png")

white_img = [pygame.image.load("assets/pieces/PawnW.png"),
             pygame.image.load("assets/pieces/RookW.png"),
             pygame.image.load("assets/pieces/KnightW.png"),
             pygame.image.load("assets/pieces/BishopW.png"),
             pygame.image.load("assets/pieces/QueenW.png"),
             pygame.image.load("assets/pieces/KingW.png"),
             pygame.image.load("assets/pieces/RookW.png"),
             pygame.image.load("assets/pieces/KingW.png")
             ]

black_img = [pygame.image.load("assets/pieces/PawnB.png"),
             pygame.image.load("assets/pieces/RookB.png"),
             pygame.image.load("assets/pieces/KnightB.png"),
             pygame.image.load("assets/pieces/BishopB.png"),
             pygame.image.load("assets/pieces/QueenB.png"),
             pygame.image.load("assets/pieces/KingB.png"),
             pygame.image.load("assets/pieces/RookB.png"),
             pygame.image.load("assets/pieces/KingB.png")
             ]

white_convert_img = [pygame.image.load("assets/pawn_transformation_UI/black_basic.png"),
                     pygame.image.load(
                         "assets/pawn_transformation_UI/black_bishop.png"),
                     pygame.image.load(
                         "assets/pawn_transformation_UI/black_knight.png"),
                     pygame.image.load(
                         "assets/pawn_transformation_UI/black_queen.png"),
                     pygame.image.load(
                         "assets/pawn_transformation_UI/black_rook.png"),
                     ]
black_convert_img = [pygame.image.load("assets/pawn_transformation_UI/black_basic.png"),
                     pygame.image.load(
                         "assets/pawn_transformation_UI/black_bishop.png"),
                     pygame.image.load(
                         "assets/pawn_transformation_UI/black_knight.png"),
                     pygame.image.load(
                         "assets/pawn_transformation_UI/black_queen.png"),
                     pygame.image.load(
                         "assets/pawn_transformation_UI/black_rook.png"),
                     ]

reset_b = pygame.image.load("assets/icons/reset.png")
font = pygame.font.Font("assets/fonts/Anonymous/Anonymous.ttf", 20)
##################################################################################
display = pygame.display.set_mode((1200, 800))
dont_show_this_piece = None
show_convert_UI = False


def is_over(x, y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if x < mouse_x < x + width:
        if y < mouse_y < y + height:
            return True
    return False


def blit_pieces(board: np.ndarray, turn, flip_board):
    start_x = 82
    start_y = 84
    piece_size = 80

    pieces = np.nonzero(np.reshape(board[:, :, 1], (8, 8)))
    for y, x in zip(pieces[0], pieces[1]):
        piece = board[y, x]
        x = get_index(x, turn, flip_board)
        y = get_index(y, turn, flip_board)
        piece_pos = (start_x + (piece_size * x), start_y + (piece_size * y))
        # white piece
        if piece[0] == 1:
            display.blit(white_img[piece[1] - 1], piece_pos)
        # black piece
        else:
            display.blit(black_img[piece[1] - 1], piece_pos)


def get_moves(board, turn, check, flip_board):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # if black turn invert
    y, x = (((mouse_y - 84) // 80), ((mouse_x - 82) // 80))
    curr_pos = (get_index(y, turn, flip_board), get_index(x, turn, flip_board))
    if curr_pos[0] < 8 and curr_pos[1] < 8:
        if turn == board[curr_pos[0], curr_pos[1], 0]:
            moves = logic.return_possible_moves(board, curr_pos, turn)
            if check:
                moves = logic.block_check_moves(board, curr_pos, moves, turn)
            return moves, curr_pos


def blit_possible_moves(shown_moves, turn, flip_board):
    for y, x in list(shown_moves.values())[0]:
        x = get_index(x, turn, flip_board)
        y = get_index(y, turn, flip_board)
        pos = (42 + (x + 1) * 80, 45 + ((y + 1) * 80))
        pygame.draw.circle(display, (138, 85, 85), pos, 16)


def blit_check(board, turn, checkmate, flip_board):
    a = board[:, :, 1]
    k_pos = np.transpose(np.concatenate((np.nonzero(a == 8), np.nonzero(a == 6)), axis=1))
    for y, x in k_pos:
        if board[y, x, 0] == turn:
            x = get_index(x, turn, flip_board)
            y = get_index(y, turn, flip_board)
            pos = (2 + ((x + 1) * 80), 6 + ((y + 1) * 80))
            break
    pygame.draw.rect(display, (138, 85, 85), (pos[0], pos[1], 80, 80))
    if not checkmate:
        color = 'White' if turn == 1 else 'Black'
        txt = font.render(f"{color} is in check", True, (255, 255, 255))
        display.blit(txt, (770, 100))


def blit_modes(board, current_mode, flip_board):
    modes = ['Player vs player on one computer', 'Player vs computer(TODO)', 'Play online']
    title = font.render('Modes: ', True, (255, 255, 255))
    # draw rectangle on selected mode
    pygame.draw.rect(display, (0, 0, 0), (750, 240 + (current_mode * 60), 500, 60))

    display.blit(title, (770, 200))
    # blit all modes
    for i in range(len(modes)):
        modes_rendered = font.render(modes[i], True, (255, 255, 255))
        display.blit(modes_rendered, (770, 260 + (i * 60)))
    # if mode 0 blit button for flipping board
    if current_mode == 0:
        txt_flip_board = font.render('Flip board', True, (255, 255, 255))
        display.blit(txt_flip_board, (1060, 210))

        # draw toggle flip board button
        pygame.draw.rect(display, (0, 0, 0), (1030, 210, 20, 20))
        if not flip_board:
            pygame.draw.rect(display, (255, 255, 255), (1032, 212, 16, 16))


def update_position(board, shown_moves, turn, flip_board):
    # if mouse is clicked over legal move piece there, update pos else return None
    mouse_x, mouse_y = pygame.mouse.get_pos()
    y, x = (mouse_y - 84) // 80, (mouse_x - 82) // 80
    wanted_pos = (get_index(y, turn, flip_board), get_index(x, turn, flip_board))
    if shown_moves:
        if wanted_pos in list(shown_moves.values())[0]:
            last_pos = list(shown_moves.keys())[0]
            return logic.update_pos(board, last_pos, wanted_pos, turn)
    return None


def blit_checkmate(turn):
    color = 'black' if turn == 1 else 'white'
    txt = font.render(f"Checkmate, {color} is victorious", True, (255, 255, 255))
    display.blit(txt, (770, 100))


def restart_clicked():
    if is_over(900, 600, 150, 150):
        return True
    return False


def modes_clicked():
    if is_over(780, 240, 300, 180):
        x, y = pygame.mouse.get_pos()
        if y < 320:
            return 0
        elif y < 380:
            return 1
        else:
            return 2
    return None


def flip_button_clicked():
    if is_over(1030, 210, 170,20):
        return True
    return False

def blit_restart_b():
    display.blit(reset_b, (900, 600))


def blit_gui(board: np.ndarray, shown_moves, check, checkmate, turn, current_mode, flip_board):
    display.blit(bg, (0, 0))
    blit_restart_b()
    blit_modes(board, current_mode, flip_board)
    if checkmate:
        blit_checkmate(turn)
    if check:
        blit_check(board, turn, checkmate, flip_board)
    blit_pieces(board, turn, flip_board)
    if shown_moves:
        blit_possible_moves(shown_moves, turn, flip_board)


def get_index(index, turn, flip_board, max_index=8):
    # if black move and invert index
    if flip_board and turn == 2:
        return max_index - index - 1

    return index
