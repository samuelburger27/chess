import pygame

import logic

pygame.init()
# load images
bg = pygame.image.load("assets/board.png")

piece_images = [
                pygame.image.load("assets/pieces/PawnB.png"),
                pygame.image.load("assets/pieces/RookB.png"),
                pygame.image.load("assets/pieces/KnightB.png"),
                pygame.image.load("assets/pieces/BishopB.png"),
                pygame.image.load("assets/pieces/QueenB.png"),
                pygame.image.load("assets/pieces/KingB.png"),

                pygame.image.load("assets/pieces/PawnW.png"),
                pygame.image.load("assets/pieces/RookW.png"),
                pygame.image.load("assets/pieces/KnightW.png"),
                pygame.image.load("assets/pieces/BishopW.png"),
                pygame.image.load("assets/pieces/QueenW.png"),
                pygame.image.load("assets/pieces/KingW.png"),
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
show_convert_UI = False


def is_over(x: int, y: int, width: int, height: int) -> bool:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if x < mouse_x < x + width:
        if y < mouse_y < y + height:
            return True
    return False


def blit_pieces(board: logic.Board, white_turn: bool, flip_board: bool) -> None:
    start_x = 82
    start_y = 84
    piece_size = 80

    pieces = board.get_all_pieces_pos()
    for y, x in pieces:
        piece = board.get_tile(y, x)
        assert piece is not None
        x = get_index(x, white_turn, flip_board)
        y = get_index(y, white_turn, flip_board)
        piece_pos = (start_x + (piece_size * x), start_y + (piece_size * y))
        display.blit(piece_images[piece], piece_pos)


def get_clicked_piece_coordinates(board: logic.Board, white_turn: bool, flip_board: bool) -> logic.pos | None:
    """return coordinates if clicked on player color piece
    None otherwise"""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # if blackwhite_turn invert
    y, x = (((mouse_y - 84) // 80), ((mouse_x - 82) // 80))
    curr_y, curr_x = get_index(y, white_turn, flip_board), get_index(x, white_turn, flip_board)
    if curr_y < 8 and curr_x < 8 and white_turn == logic.is_white(board.get_tile(curr_y, curr_x)):
        return curr_y, curr_x
    return None


def blit_possible_moves(shown_moves: set[logic.pos], white_turn: bool, flip_board: bool) -> None:
    for y, x in shown_moves:
        x = get_index(x, white_turn, flip_board)
        y = get_index(y, white_turn, flip_board)
        pos = (42 + (x + 1) * 80, 45 + ((y + 1) * 80))
        pygame.draw.circle(display, (138, 85, 85), pos, 16)


def blit_check(board: logic.Board, white_turn: bool, checkmate: bool, flip_board: bool) -> None:
    king_y, king_x = board.get_king_position(white_turn)
    y = get_index(king_y, white_turn, flip_board)
    x = get_index(king_x, white_turn, flip_board)
    pos = (2 + ((x + 1) * 80), 6 + ((y + 1) * 80))

    pygame.draw.rect(display, (138, 85, 85), (pos[0], pos[1], 80, 80))
    if not checkmate:
        color = 'White' if white_turn else 'Black'
        txt = font.render(f"{color} is in check", True, (255, 255, 255))
        display.blit(txt, (770, 100))


def blit_modes(current_mode: int, flip_board: bool) -> None:
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


def update_position(board: logic.Board, last_pos: logic.pos | None, shown_moves: set[logic.pos], white_turn: bool,
                    flip_board: bool) -> logic.Board | None:
    # if mouse is clicked over legal move piece there, update pos else return None
    mouse_x, mouse_y = pygame.mouse.get_pos()
    y, x = (mouse_y - 84) // 80, (mouse_x - 82) // 80
    wanted_pos = (get_index(y, white_turn, flip_board), get_index(x, white_turn, flip_board))
    if wanted_pos in shown_moves and last_pos is not None:
        return logic.update_pos(board, last_pos, wanted_pos, white_turn)
    return None


def blit_checkmate(white_turn: bool) -> None:
    color = 'black' if white_turn == 1 else 'white'
    txt = font.render(f"Checkmate, {color} is victorious", True, (255, 255, 255))
    display.blit(txt, (770, 100))


def restart_clicked() -> bool:
    return is_over(900, 600, 150, 150)


def is_modes_clicked() -> bool:
    return is_over(780, 240, 300, 180)


def change_modes() -> int:
    _, y = pygame.mouse.get_pos()
    if y < 320:
        return 0
    elif y < 380:
        return 1
    return 2


def flip_button_clicked() -> bool:
    return is_over(1030, 210, 170, 20)


def blit_restart_b() -> None:
    display.blit(reset_b, (900, 600))


def blit_gui(board: logic.Board, shown_moves: set[logic.pos], check: bool, checkmate: bool,
             white_turn: bool, current_mode: int, flip_board: bool) -> None:
    display.blit(bg, (0, 0))
    blit_restart_b()
    blit_modes(current_mode, flip_board)
    if checkmate:
        blit_checkmate(white_turn)
    if check:
        blit_check(board, white_turn, checkmate, flip_board)
    blit_pieces(board, white_turn, flip_board)
    if shown_moves:
        blit_possible_moves(shown_moves, white_turn, flip_board)


def get_index(index: int, white_turn: bool, flip_board: bool, max_index: int = 8) -> int:
    # if black move and invert index
    if flip_board and not white_turn:
        return max_index - index - 1
    return index
