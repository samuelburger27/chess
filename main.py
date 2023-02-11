import pygame
import numpy as np
import GUI
import logic

run = True
mouse_down = False
game_over = False
board = logic.restart_pieces(np.zeros((8, 8, 2))).astype(int)

if __name__ == '__main__':
    while run:
        GUI.blit_gui(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
