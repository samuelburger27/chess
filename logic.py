
import GUI
import pygame
import time


kicked_pieces = []
current_turn = 0


class playing_pieces():
    """
    0. pawn
    1. rook
    2. knight
    3. bishop
    4. queen
    5. king

    //////////////////
    0. white
    1. black
    """

    def __init__(self, piece, color, id, curr_position):
        self.piece = piece
        self.color = color
        self.curr_x, self.curr_y = curr_position
        self.id = id
        self.posible_moves = []

    def is_mouse_over(self, pos):
        # return true if this piece is clicked
        x, y = pos
        grid_x, grid_y = GUI.grid()[self.curr_y][self.curr_x]
        if (x > grid_x and x < grid_x+80) and (y > grid_y and y < grid_y+80):
            return True
        return False

    def get_current_position(self):
        return (self.curr_x, self.curr_y)

    def pawn_rules(self):
        # TOCOMPLETE
        # prememnu na queen alebo bishup
        if self.curr_y >= 1 and self.curr_y <= 6:  # check if its the edge of map
            if self.color == 0:
                # if its starting position so pawn can move 2 blocks
                if self.curr_y == 6:
                    self.posible_moves.append((self.curr_x, self.curr_y-2))
                self.posible_moves.append((self.curr_x, self.curr_y-1))

                for pcs in pieces:
                    for compr in self.posible_moves:
                        if pcs.get_current_position() == compr:
                            self.posible_moves.pop(
                                self.posible_moves.index(compr))

                for p in pieces:
                    if p.color == 1:
                        x, y = p.get_current_position()

                        if self.get_current_position() == (x+1, y+1):
                            self.posible_moves.append((x, y))
                        if self.get_current_position() == (x-1, y+1):
                            self.posible_moves.append((x, y))
            else:
                if self.curr_y == 1:
                    self.posible_moves.append((self.curr_x, self.curr_y+2))
                self.posible_moves.append((self.curr_x, self.curr_y+1))

                for pcs in pieces:
                    for compr in self.posible_moves:
                        if pcs.get_current_position() == compr:
                            self.posible_moves.pop(
                                self.posible_moves.index(compr))

                for p in pieces:
                    if p.color == 0:
                        x, y = p.get_current_position()
                        if self.get_current_position() == (x+1, y-1):
                            self.posible_moves.append((x, y))
                        if self.get_current_position() == (x-1, y-1):
                            self.posible_moves.append((x, y))

    def rook_rules(self):
        boardering_pieces = []
        x_plus = False
        x_minus = False
        y_plus = False
        y_minus = False

        def is_there(x, y):
            for pcs in boardering_pieces:
                if pcs.get_current_position() == (x, y):
                    print("YEA")
                    # if pcs.color == self.color:
                    #     self.posible_moves.pop(
                    #         self.posible_moves.index((x, y)))
                    return True
            return False

        for xs in range(8):
            if xs != self.curr_x:
                self.posible_moves.append((xs, self.curr_y))
            if xs != self.curr_y:
                self.posible_moves.append((self.curr_x, xs))

        for pcs in pieces:
            if (pcs.curr_x == self.curr_x and pcs.id != self.id) or (pcs.curr_y == self.curr_y and pcs.id != self.id):
                boardering_pieces.append(pcs)

        for i in range(8):
            if self.curr_x+i < 8:
                if is_there(self.curr_x+i, self.curr_y) and not x_plus:
                    x_plus = True
                elif x_plus == True:
                    self.posible_moves.pop(self.posible_moves.index(
                        (self.curr_x+i, self.curr_y)))

            if self.curr_x-i > 0:
                if is_there(self.curr_x-i, self.curr_y) and not x_minus:
                    x_minus = True
                elif x_minus == True:
                    self.posible_moves.pop(self.posible_moves.index(
                        (self.curr_x-i, self.curr_y)))

            if self.curr_y+i < 8:
                if is_there(self.curr_x, self.curr_y+1) and not y_plus:
                    y_plus = True
                elif y_plus == True:
                    self.posible_moves.pop(self.posible_moves.index(
                        (self.curr_x, self.curr_y+1)))

            if self.curr_y-i > 0:
                if is_there(self.curr_x, self.curr_y-1) and not y_minus:
                    y_minus = True
                elif y_minus == True:
                    self.posible_moves.pop(self.posible_moves.index(
                        (self.curr_x, self.curr_y-1)))

    def get_rules_for_current_piece(self):
        if self.piece == 0:
            self.pawn_rules()
        if self.piece == 1:
            self.rook_rules()
        return self.posible_moves

    def clear_posibble_moves(self):
        self.posible_moves = []


def restart_pieces():
    global pieces
    pieces = [playing_pieces(0, 0, 0, (0, 6)),
              playing_pieces(0, 0, 1, (1, 6)),
              playing_pieces(0, 0, 2, (2, 6)),
              playing_pieces(0, 0, 3, (3, 6)),
              playing_pieces(0, 0, 4, (4, 6)),
              playing_pieces(0, 0, 5, (5, 6)),
              playing_pieces(0, 0, 6, (6, 6)),
              playing_pieces(0, 0, 7, (7, 6)),

              playing_pieces(1, 0, 8, (0, 7)),
              playing_pieces(2, 0, 9, (1, 7)),
              playing_pieces(3, 0, 10, (2, 7)),
              playing_pieces(4, 0, 11, (3, 7)),
              playing_pieces(5, 0, 12, (4, 7)),
              playing_pieces(3, 0, 13, (5, 7)),
              playing_pieces(2, 0, 14, (6, 7)),
              playing_pieces(1, 0, 15, (7, 7)),



              playing_pieces(0, 1, 16, (0, 1)),
              playing_pieces(0, 1, 17, (1, 1)),
              playing_pieces(0, 1, 18, (2, 1)),
              playing_pieces(0, 1, 19, (3, 1)),
              playing_pieces(0, 1, 20, (4, 1)),
              playing_pieces(0, 1, 21, (5, 1)),
              playing_pieces(0, 1, 22, (6, 1)),
              playing_pieces(0, 1, 23, (7, 1)),

              playing_pieces(1, 1, 24, (0, 0)),
              playing_pieces(2, 1, 25, (1, 0)),
              playing_pieces(3, 1, 26, (2, 0)),
              playing_pieces(4, 1, 27, (3, 0)),
              playing_pieces(5, 1, 28, (4, 0)),
              playing_pieces(3, 1, 29, (5, 0)),
              playing_pieces(2, 1, 30, (6, 0)),
              playing_pieces(1, 1, 31, (7, 0)),
              ]


def clicked_on_piece(mouse_pos):
    # find which piece was clicked
    for pcs in pieces:
        if pcs.is_mouse_over(mouse_pos):
            return pcs


def find_wanted_destiantion():
    # find on which positiion in grid the mouse is right now
    for i in range(8):
        for j in range(8):
            grid_x, grid_y = GUI.grid()[i][j]
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if (mouse_x > grid_x and mouse_x < grid_x+80) and (mouse_y > grid_y and mouse_y < grid_y+80):
                return (j, i)


def update_piece_pos(piece):
    global current_turn
    # check if its correct turn to go for the color
    if current_turn % 2 == piece.color:
        for lst in piece.posible_moves:
            if lst == find_wanted_destiantion():
                piece.curr_x = find_wanted_destiantion()[0]
                piece.curr_y = find_wanted_destiantion()[1]

                if is_kicked(find_wanted_destiantion(), piece):
                    # if we found pieces with same position kick bottom piece
                    #  and move it into kicked_pieces list
                    kicked_pieces.append(pieces.pop(
                        pieces.index(is_kicked(find_wanted_destiantion(), piece))))

                current_turn += 1
                piece.clear_posibble_moves()
                break


def is_kicked(pos, rhs):
    for piece in pieces:
        if piece.id != rhs.id and piece.color != rhs.color:
            if piece.get_current_position() == pos:
                return piece
    return False
