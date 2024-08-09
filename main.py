import pygame
import GUI
import logic


if __name__ == '__main__':
    # TODO add turns - done
    # TODO add check detection and show only moves which will block check - done
    # TODO not allow moves which will put player in check - done
    # TODO add check mate -done
    # TODO add pawn promotion - kida done XD
    # TODO add drag functionality
    # TODO add move history
    # TODO wlan playability
    # TODO add en peasant
    run = True
    white_turn = True
    current_mode = 0
    flip_board = True
    shown_moves: set[logic.pos] = set()
    clicked_piece: logic.pos | None = None
    check = False
    checkmate = False
    board = logic.Board()
    while run:
        GUI.blit_gui(board, shown_moves, check, checkmate, white_turn, current_mode, flip_board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # TODO
                pass
            if event.type == pygame.MOUSEBUTTONUP:
                print(pygame.mouse.get_pos())
                # if clicked on modes
                if GUI.is_modes_clicked():
                    current_mode = GUI.change_modes()

                # if clicked on flip board button
                if current_mode == 0:
                    if GUI.flip_button_clicked():
                        flip_board = not flip_board
                # if clicked on reset butt
                if GUI.restart_clicked():
                    board.restart_board()
                    white_turn = True
                    shown_moves = set()
                    check = False
                    checkmate = False
                    pawn_promote = False
                    flip_board = True
                else:
                    new_board = GUI.update_position(board, clicked_piece, shown_moves, white_turn, flip_board)
                    if new_board is not None:
                        board = new_board
                        shown_moves = set()
                        white_turn = not white_turn
                        check = logic.is_check(board, white_turn)
                        if check:
                            if logic.game_over(board, white_turn):
                                checkmate = True
                    else:
                        clicked_coords = GUI.get_clicked_piece_coordinates(board, white_turn, flip_board)
                        if clicked_coords is not None:
                            clicked_piece = clicked_coords
                            shown_moves = set(logic.return_possible_moves(board, clicked_piece, white_turn))

        pygame.display.update()

    pygame.quit()
