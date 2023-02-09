import pygame

import GUI
import logic

run = True
mouse_down = False
game_over = False

logic.restart_pieces()
GUI.grid()
while run:
    GUI.display()

    GUI.show_pieces()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not mouse_down:
                    clicked_piece = logic.clicked_on_piece(
                        pygame.mouse.get_pos())
                    mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                GUI.dont_show_this_piece = None
                if clicked_piece != None:
                    logic.update_piece_pos(clicked_piece)
                    logic.clear_all_poss_moves()
                    if logic.find_check(logic.pieces) != 0:
                        a = logic.find_possible_moves_for_check(
                            logic.find_check(logic.pieces))
                        logic.clear_all_poss_moves()
                        if len(a) > 0:
                            for i in len(a):
                                for piece in logic.pieces:
                                    if piece.id == i[0]:
                                        piece.posible_moves = i[1]
                        print(a)
    if mouse_down:
        # if mouse is held down and piece was clicked move the piece
        if clicked_piece != None:
            GUI.piece_follow_mouse(clicked_piece)
            GUI.show_posibble_moves(
                clicked_piece.get_rules_for_current_piece())
    pygame.display.update()

pygame.quit()
