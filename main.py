import pygame
import numpy as np
import GUI
import logic


if __name__ == '__main__':
    run = True
    game_over = False
    turn = 0
    shown_moves = {}
    board = logic.restart_pieces(np.zeros((8, 8, 2))).astype(int)
    while run:
        GUI.blit_gui(board, shown_moves)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = GUI.update_position(board, shown_moves)
                if pos is not None:
                    board = pos
                    shown_moves = {}
                    if turn == 0:
                        turn = 1
                    else:
                        turn = 0
                else:
                    shown_moves = {}
                    moves, cords = GUI.get_moves(board, shown_moves, turn)
                    shown_moves[cords] = moves

        pygame.display.update()

    pygame.quit()
