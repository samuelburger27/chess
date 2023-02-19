import numpy as np


def restart_pieces(board: np.ndarray):
    """
    0- empty space
    1- pawn
    2- rook(can castle)
    3- knight
    4- bishop
    5- queen
    6- king (can castle)
    7- rook(cant castle)
    8- king(cant castle)
    """
    # pawns
    board[6, 0] = [1, 1]
    board[6, 1] = [1, 1]
    board[6, 2] = [1, 1]
    board[6, 3] = [1, 1]
    board[6, 4] = [1, 1]
    board[6, 5] = [1, 1]
    board[6, 6] = [1, 1]
    board[6, 7] = [1, 1]

    # rooks
    board[7, 0] = [1, 2]
    board[7, 7] = [1, 2]

    # knights
    board[7, 1] = [1, 3]
    board[7, 6] = [1, 3]

    # bishops
    board[7, 2] = [1, 4]
    board[7, 5] = [1, 4]

    # queen
    board[7, 3] = [1, 5]

    # king
    board[7, 4] = [1, 6]

    # ################################################### black
    # pawns
    board[1, 0] = [2, 1]
    board[1, 1] = [2, 1]
    board[1, 2] = [2, 1]
    board[1, 3] = [2, 1]
    board[1, 4] = [2, 1]
    board[1, 5] = [2, 1]
    board[1, 6] = [2, 1]
    board[1, 7] = [2, 1]

    # rooks
    board[0, 0] = [2, 2]
    board[0, 7] = [2, 2]

    # knights
    board[0, 1] = [2, 3]
    board[0, 6] = [2, 3]

    # bishops
    board[0, 2] = [2, 4]
    board[0, 5] = [2, 4]

    # queen
    board[0, 3] = [2, 5]

    # king
    board[0, 4] = [2, 6]

    return board


def return_possible_moves(board, piece_index):
    """return all possible moves for piece"""
    y, x = piece_index
    colour, id = board[y, x]
    moves = []
    castle = 0

    def blank():
        # blank space
        pass

    def pawn():
        # white
        if colour == 1:
            direction = y - 1
            start_pos = 6
            start_move = y - 2
        # black
        else:
            direction = y + 1
            start_pos = 1
            start_move = y + 2

        if x < 7:
            if board[direction, x + 1, 0] != colour and board[direction, x + 1, 0] != 0:
                moves.append((direction, x + 1))
        if x > 0:
            if board[direction, x - 1, 0] != colour and board[direction, x - 1, 0] != 0:
                moves.append((direction, x - 1))
        if (board[direction, x] == np.zeros(2)).all():
            moves.append((direction, x))
            if y == start_pos and (board[start_move, x] == np.zeros(2)).all():
                moves.append((start_move, x))

    # rook
    def rook():
        # add all moves in 4 direction until hit your or enemy piece
        y_pos_stop = 0
        y_neg_stop = 0
        x_pos_stop = 0
        x_neg_stop = 0
        for i in range(1, 8):
            if y + i <= 7 and not y_pos_stop:
                if board[y + i, x, 0] != colour:
                    moves.append((y + i, x))
                    # if enemy piece
                    if board[y + i, x, 0] != 0:
                        y_pos_stop = 1
                # no piece
                else:
                    y_pos_stop = 1
            if y - i >= 0 and not y_neg_stop:
                if board[y - i, x, 0] != colour:
                    moves.append((y - i, x))
                    if board[y - i, x, 0] != 0:
                        y_neg_stop = 1
                else:
                    y_neg_stop = 1
            if x + i <= 7 and not x_pos_stop:
                if board[y, x + i, 0] != colour:
                    moves.append((y, x + i))
                    if board[y, x + i, 0] != 0:
                        x_pos_stop = 1
                else:
                    x_pos_stop = 1
            if x - i >= 0 and not x_neg_stop:
                if board[y, x - i, 0] != colour:
                    moves.append((y, x - i))
                    if board[y, x - i, 0] != 0:
                        x_neg_stop = 1
                else:
                    x_neg_stop = 1

    # knight
    def knight():
        """check all 8 possible knight moves"""
        if y + 2 < 8:
            if x + 1 < 8:
                if board[y + 2, x + 1, 0] != colour:
                    moves.append((y + 2, x + 1))
            if x - 1 >= 0:
                if board[y + 2, x - 1, 0] != colour:
                    moves.append((y + 2, x - 1))

        if y - 2 >= 0:
            if x + 1 < 8:
                if board[y - 2, x + 1, 0] != colour:
                    moves.append((y - 2, x + 1))
            if x - 1 >= 0:
                if board[y - 2, x - 1, 0] != colour:
                    moves.append((y - 2, x - 1))

        if x + 2 < 8:
            if y + 1 < 8:
                if board[y + 1, x + 2, 0] != colour:
                    moves.append((y + 1, x + 2))
            if y - 1 >= 0:
                if board[y - 1, x + 2, 0] != colour:
                    moves.append((y - 1, x + 2))

        if x - 2 >= 0:
            if y + 1 < 8:
                if board[y + 1, x - 2, 0] != colour:
                    moves.append((y + 1, x - 2))
            if y - 1 >= 0:
                if board[y - 1, x - 2, 0] != colour:
                    moves.append((y - 1, x - 2))

    # bishop
    def bishop():
        y_p_x_p = 0
        y_n_x_p = 0
        y_p_x_n = 0
        y_n_x_n = 0
        for i in range(1, 8):
            if y + i <= 7 and x + i <= 7 and not y_p_x_p:
                if board[y + i, x + i, 0] != colour:
                    moves.append((y + i, x + i))
                    # if enemy piece
                    if board[y + i, x + i, 0] != 0:
                        y_p_x_p = 1
                # no piece
                else:
                    y_p_x_p = 1
            if y - i >= 0 and x + i <= 7 and not y_n_x_p:
                if board[y - i, x + i, 0] != colour:
                    moves.append((y - i, x + i))

                    if board[y - i, x + i, 0] != 0:
                        y_n_x_p = 1
                else:
                    y_n_x_p = 1
            if y + i <= 7 and x - i >= 0 and not y_p_x_n:
                if board[y + i, x - i, 0] != colour:
                    moves.append((y + i, x - i))

                    if board[y + i, x - i, 0] != 0:
                        y_p_x_n = 1
                else:
                    y_p_x_n = 1
            if y - i >= 0 and x - i >= 0 and not y_n_x_n:
                if board[y - i, x - i, 0] != colour:
                    moves.append((y - i, x - i))

                    if board[y - i, x - i, 0] != 0:
                        y_n_x_n = 1
                else:
                    y_n_x_n = 1

    # queen
    def queen():
        rook()
        bishop()

    def king():
        # castle
        if id == 6:
            # queen side
            # if space between king and rook is clear
            if (board[y, 1:3] == np.zeros(2)).all():
                moves.append((y, 2))
            # king side
            if (board[y, 5:6] == np.zeros(2)).all():
                moves.append((y, 6))

        if y + 1 <= 7:
            if x + 1 <= 7:
                if board[y + 1, x + 1, 0] != colour:
                    moves.append((y + 1, x + 1))
            if x - 1 >= 0:
                if board[y + 1, x - 1, 0] != colour:
                    moves.append((y + 1, x - 1))
            if board[y + 1, x, 0] != colour:
                moves.append((y + 1, x))
        if y - 1 >= 0:
            if x + 1 <= 7:
                if board[y - 1, x + 1, 0] != colour:
                    moves.append((y - 1, x + 1))
            if x - 1 >= 0:
                if board[y - 1, x - 1, 0] != colour:
                    moves.append((y - 1, x - 1))
            if board[y - 1, x, 0] != colour:
                moves.append((y - 1, x))
        if x + 1 <= 7:
            if board[y, x + 1, 0] != colour:
                moves.append((y, x + 1))
        if x - 1 >= 0:
            if board[y, x - 1, 0] != colour:
                moves.append((y, x - 1))

    list_of_func = [blank, pawn, rook, knight, bishop, queen, king, rook, king]
    list_of_func[id]()
    return moves

def get_all_moves(board: np.ndarray, turn: int, get_list=False):
    all_moves = {}
    list_of_moves = []
    a = board[:, :, 0]
    playing_pieces = np.nonzero(a == turn)
    for y, x in zip(playing_pieces[0], playing_pieces[1]):
        all_moves[(y, x)] = return_possible_moves(board, (y, x))
        list_of_moves.extend(return_possible_moves(board, (y, x)))
    if not get_list:
        return all_moves
    return list_of_moves


def check(board, turn):
    a = board[:, :, 1]
    pos = None
    # get position of all kings(both colors, both id)
    k_pos = np.transpose(np.concatenate((np.nonzero(a == 8), np.nonzero(a == 6)), axis=1))
    for y, x in k_pos:
        if board[y, x, 0] != turn:
            pos = tuple((y, x))
            break
    if pos in get_all_moves(board, turn, True):
        return True
    return False


def update_pos(board, last_pos, wanted_pos, turn):
    wanted_y, wanted_x = wanted_pos
    last_y, last_x = last_pos

    # check castling
    if board[last_y, last_x, 1] == 6:
        # king side
        if wanted_x - last_x == 2:
            board[wanted_y, last_x + 1] = board[wanted_y, 7]
            board[wanted_y, last_x + 2] = board[last_y, last_x]
            board[last_y, last_x], board[wanted_y, 7] = np.zeros(2)
        # queen side
        elif wanted_x - last_x == -2:
            board[wanted_y, last_x - 1] = board[wanted_y, 0]
            board[wanted_y, last_x - 2] = board[last_y, last_x]
            board[last_y, last_x], board[wanted_y, 0] = np.zeros(2)

    else:
        board[wanted_y, wanted_x] = board[last_y, last_x]
        board[last_y, last_x] = np.zeros(2)
    # if king or rook moved change id to non castleble ones
    if board[wanted_y, wanted_x, 1] == 2:
        board[wanted_y, wanted_x, 1] = 7
    elif board[wanted_y, wanted_x, 1] == 6:
        board[wanted_y, wanted_x, 1] = 8

    ch = check(board, turn)
    print(ch)
    return board, ch


def block_check_moves(board, turn):
    # TODO castle possibility
    dic = get_all_moves(board, turn)
    for piece, moves in dic.items():
        for pos in moves:
            if update_pos(board, piece, pos, turn)[1]:
                pass
        pass
    pass
