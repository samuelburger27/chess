import pygame
import numpy as np
import GUI
import logic


if __name__ == '__main__':
    # TODO add turns - done
    # TODO add pawn promotion
    # TODO add check detection and show only moves which will block check - done
    # TODO not allow moves which will put player in check
    # TODO add check mate
    # TODO add drag functionality
    run = True
    game_over = False
    # 1- white, 2- black
    turn = 1
    shown_moves = {}
    check = 0
    board = logic.restart_pieces(np.zeros((8, 8, 2))).astype(int)
    while run:
        GUI.blit_gui(board, shown_moves)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = GUI.update_position(board, shown_moves, turn)
                if pos is not None:
                    board = pos
                    shown_moves = {}
                    if turn == 1:
                        turn = 2
                    else:
                        turn = 1
                    check = logic.check(board, turn)
                    if check:
                        logic.game_over(board, turn)
                else:
                    if GUI.get_moves(board, turn, check):
                        moves, cords = GUI.get_moves(board, turn, check)
                        shown_moves = {cords: moves}
        pygame.display.update()

    pygame.quit()
