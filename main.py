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
    run = True
    # 1- white, 2- black
    turn = 1
    shown_moves = {}
    check = 0
    checkmate = False
    board = logic.restart_pieces()
    while run:
        GUI.blit_gui(board, shown_moves, check, checkmate, turn)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # TODO
                pass
            if event.type == pygame.MOUSEBUTTONUP:
                if not GUI.restart_clicked():
                    pos = GUI.update_position(board, shown_moves, turn)
                    if pos is not None:
                        board = pos
                        shown_moves = {}
                        turn = 2 if turn == 1 else 1
                        check = logic.check(board, turn)
                        if check:
                            if logic.game_over(board, turn):
                                checkmate = True
                    else:
                        if GUI.get_moves(board, turn, check):
                            moves, cords = GUI.get_moves(board, turn, check)
                            shown_moves = {cords: moves}
                else:
                    board = logic.restart_pieces()
                    turn = 1
                    shown_moves = {}
                    check = 0
                    checkmate = False
                    pawn_promote = False

        pygame.display.update()

    pygame.quit()
