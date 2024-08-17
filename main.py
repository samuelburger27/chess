import pygame
import GUI
import logic


if __name__ == '__main__':
    run = True
    current_mode = 0
    flip_board = True
    shown_moves: set[logic.pos] = set()
    clicked_piece: logic.pos | None = None
    chess = logic.ChessGame()
    while run:
        GUI.blit_gui(chess, shown_moves, current_mode, flip_board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                # if clicked on modes
                if GUI.is_modes_clicked():
                    current_mode = GUI.change_modes()

                # if clicked on flip board button
                if current_mode == 0:
                    if GUI.flip_button_clicked():
                        flip_board = not flip_board
                # if clicked on reset butt
                if GUI.restart_clicked():
                    chess.restart_game()
                    shown_moves = set()
                    flip_board = True
                else:
                    wanted_cord = GUI.clicked_on_poss_move(chess, clicked_piece, shown_moves, flip_board)
                    if wanted_cord is not None:
                        assert clicked_piece is not None
                        chess.make_move(clicked_piece, wanted_cord)
                        shown_moves = set()
                    else:
                        clicked_coords = GUI.get_clicked_piece_coordinates(chess, flip_board)
                        if clicked_coords is not None:
                            clicked_piece = clicked_coords
                            shown_moves = set(chess.return_possible_moves(clicked_piece))

        pygame.display.update()

    pygame.quit()
