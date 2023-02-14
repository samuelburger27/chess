
import pygame
import numpy as np


class PlayingPiece:
    """
      1. pawn
      2. rook
      3. knight
      4. bishop
      5. queen
      6. king

      //////////////////
      0. white
      1. black
    """

    def __init__(self, piece, color, id, curr_position):
        self.piece = piece
        self.color = color
        self.curr_x, self.curr_y = curr_position
        self.id = id
        self.possible_moves = []


def restart_pieces(board: np.ndarray):
    """
    1-8 white pawns
    9-16 other white pieces
    1-29 : white colour
    30+ : black colour
    """
    # #######################white
    # pawns
    board[6, 0] = [1, 1]
    board[6, 1] = [2, 1]
    board[6, 2] = [3, 1]
    board[6, 3] = [4, 1]
    board[6, 4] = [5, 1]
    board[6, 5] = [6, 1]
    board[6, 6] = [7, 1]
    board[6, 7] = [8, 1]

    # rooks
    board[7, 0] = [9, 2]
    board[7, 7] = [10, 2]

    # knights
    board[7, 1] = [11, 3]
    board[7, 6] = [12, 3]

    # bishops
    board[7, 2] = [13, 4]
    board[7, 5] = [14, 4]

    # queen
    board[7, 3] = [15, 5]

    # king
    board[7, 4] = [16, 6]

    # ################################################### black
    # pawns
    board[1, 0] = [31, 1]
    board[1, 1] = [32, 1]
    board[1, 2] = [33, 1]
    board[1, 3] = [34, 1]
    board[1, 4] = [35, 1]
    board[1, 5] = [36, 1]
    board[1, 6] = [37, 1]
    board[1, 7] = [38, 1]

    # rooks
    board[0, 0] = [39, 2]
    board[0, 7] = [40, 2]

    # knights
    board[0, 1] = [41, 3]
    board[0, 6] = [42, 3]

    # bishops
    board[0, 2] = [43, 4]
    board[0, 5] = [44, 4]

    # queen
    board[0, 3] = [45, 5]

    # king
    board[0, 4] = [46, 6]

    return board


def return_possible_moves(board, piece_index):
    """return all possible moves for piece"""
    y, x = piece_index

    piece_id, piece_name = board[y, x]
    moves = []
    def get_colour():
        # if white
        if piece_id < 30:
            return True
        return False
    #TODO other pieces
    #TODO chcek colors of the pawns
    # pawn
    if piece_name == 1:
        if get_colour():
            direction = y-1
        else:
            direction = y+1
        if x < 7:
            if (board[direction, x+1] != np.zeros(2)).all():
                moves.append((direction, x+1))
        if x > 0:
            if (board[direction, x-1, 0] != np.zeros(2)).all():
                moves.append((direction, x-1))
        if (board[direction, x] == np.zeros(2)).all():
            moves.append((direction, x))

    # rook
    elif piece_name == 2:
        pass
    # knight
    elif piece_name == 3:
        pass
    # bishop
    elif piece_name == 4:
        pass
    # queen
    elif piece_name == 5:
        pass
    # king
    else:
        pass

    return moves

# !!!possibly not needed
def return_all_possible_moves(board: np.ndarray, turn: int):
    playing_pieces = np.reshape(board[:, :, 0], (8, 8))
    all_moves = {}
    if turn == 0:
        # get white pieces
        playing_pieces = np.nonzero(0 < playing_pieces < 30)
    else:
        playing_pieces = np.nonzero(playing_pieces > 30)
    # TODO add check checker XD
    for y, x in zip(playing_pieces[0], playing_pieces[1]):
        all_moves[playing_pieces[y][x]] = return_possible_moves(board, (y, x))

    return all_moves

def find_check(list_of_pieces):
    # find both kings
    for i in pieces:
        if i.piece == 5:
            if i.color == 0:
                white_king = i
            else:
                black_king = i

    # check if any posiblle move is attacking king
    for pc in pieces:
        if pc.id != white_king and pc.id != black_king:
            if pc.color != white_king.color:
                for a in pc.possible_moves:
                    if a == white_king.get_current_position():
                        print("White has check !!!")
                        return 1
            else:
                for a in pc.possible_moves:
                    if a == black_king.get_current_position():
                        print("Black has check !!!")
                        return 2

    return 0


def is_kicked(pos, rhs):
    for piece in pieces:
        if piece.id != rhs.id and piece.color != rhs.color:
            if piece.get_current_position() == pos:
                return piece
    return False


def find_possible_moves_for_check(color):
    # we create new copy of all pieces and their possible moves and run find check() for every possilbe moves
    # if we find that some move block check mate we put it in new list
    test_pieces = pieces.copy()
    moves_that_save_king = []
    color -= 1
    for piece in test_pieces:
        if piece.color == color:
            for moves in piece.possible_moves:
                x = piece.curr_x
                y = piece.curr_y

                piece.curr_x = moves[0]
                piece.curr_y = moves[1]
                print("Hell yea")
                if find_check(test_pieces) == 0:
                    moves_that_save_king.append([piece.id, moves])

                piece.curr_x = x
                piece.curr_y = y
    return moves_that_save_king
