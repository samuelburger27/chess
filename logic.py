import copy

import numpy as np

BLACK_ROOK = 0
BLACK_KNIGHT = 1
BLACK_BISHOP = 2
BLACK_QUEEN = 3
BLACK_KING = 4
BLACK_PAWN = 5
WHITE_ROOK = 6
WHITE_KNIGHT = 7
WHITE_BISHOP = 8
WHITE_QUEEN = 9
WHITE_KING = 10
WHITE_PAWN = 11

Tile = int | None
pos = tuple[int, int]


class Board:
    """
    Represent board using 12 numbers
    Each number represent 64 bits of information
    Each number encode position of 1 type of piece
    """

    def __init__(self) -> None:
        self.board = np.zeros(8)
        self.restart_board()

    def restart_board(self) -> None:
        self.board[BLACK_ROOK] = 0b1000000100000000000000000000000000000000000000000000000000000000
        self.board[BLACK_KNIGHT] = 0b0100001000000000000000000000000000000000000000000000000000000000
        self.board[BLACK_BISHOP] = 0b0010010000000000000000000000000000000000000000000000000000000000
        self.board[BLACK_QUEEN] = 0b0001000000000000000000000000000000000000000000000000000000000000
        self.board[BLACK_KING] = 0b0000100000000000000000000000000000000000000000000000000000000000
        self.board[BLACK_PAWN] = 0b11111111000000000000000000000000000000000000000000000000

        self.board[WHITE_ROOK] = 0b10000001
        self.board[WHITE_KNIGHT] = 0b01000010
        self.board[WHITE_BISHOP] = 0b00100100
        self.board[WHITE_QUEEN] = 0b00010000
        self.board[WHITE_KING] = 0b00001000
        self.board[WHITE_PAWN] = 0b1111111100000000

    def get_bit_sum(self, color: int | None = None) -> int:
        result = 0
        start = WHITE_ROOK if color == 0 else 0
        end = WHITE_ROOK if color == 1 else 12
        for i in range(start, end):
            result |= self.board[i]
        return result

    def get_bit_index(self, coordinates: pos) -> int:
        y, x = coordinates
        return y * 8 + x

    def get_coordinates(self, bit_index: int) -> pos:
        y = bit_index // 8
        x = bit_index % 8
        return y, x

    def get_tile(self, y: int, x: int) -> Tile:
        bit_index = self.get_bit_index((y, x))
        bit_mask = 1 << bit_index
        for i in range(12):
            if (self.board[i] & bit_mask) != 0:
                return i
        return None

    def replace_tile(self, y: int, x: int, new_tile: Tile) -> None:
        bit_mask = 1 << self.get_bit_index((y, x))
        for i in range(12):
            self.board[i] ^= bit_mask
        if new_tile is not None:
            self.board[new_tile] |= bit_mask

    def move_piece(self, old_cord: pos, new_cord: pos) -> Tile:
        new_y, new_x = new_cord
        old_y, old_x = old_cord
        piece = self.get_tile(old_y, old_x)
        removed_piece = self.get_tile(new_y, new_x)
        self.replace_tile(old_y, old_x, None)
        self.replace_tile(new_y, new_x, piece)
        return removed_piece

    def tile_is_empty(self, y: int, x: int) -> bool:
        return self.get_tile(y, x) is None

    def range_is_empty(self, rng: list[pos]) -> bool:
        for y, x in rng:
            if not self.tile_is_empty(y, x):
                return False
        return True

    def get_all_pieces_pos(self, color: int | None = None) -> list[pos]:
        """get coordinates of every piece"""
        pieces: list[pos] = []
        board_sum = self.get_bit_sum(color)
        for i in range(8 * 8):
            bit_mask = 1 << i
            if (board_sum & bit_mask) != 0:
                pieces.append(self.get_coordinates(i))
        return pieces

    # TODO maybe delete
    def get_piece_position(self, piece: int) -> list[pos]:
        position: list[pos] = []
        for i in range(8 * 8):
            bit_mask = 1 << i
            if (self.board[piece] & bit_mask) != 0:
                position.append(self.get_coordinates(i))
        return position

    def get_king_position(self, white: bool) -> pos:
        king = WHITE_KING if white else BLACK_KING
        for i in range(8 * 8):
            bit_mask = 1 << i
            if (self.board[king] & bit_mask) != 0:
                return self.get_coordinates(i)
        assert False


def is_white(tile: Tile) -> bool:
    return tile is not None and tile > BLACK_PAWN


def get_piece_moves(board: Board, piece_cord: pos) -> list[pos]:
    """return all possible moves for piece"""
    y, x = piece_cord
    piece = board.get_tile(y, x)
    if piece is None:
        return []
    piece_is_white = is_white(piece)
    moves = []

    def pawn() -> None:
        if piece_is_white:
            forward = y - 1
            start_pos = 6
            double_y = 4
        else:
            forward = y + 1
            start_pos = 1
            double_y = 3

        # enemy piece on diagonal
        if (x < 7 and board.get_tile(forward, x + 1) is not None
                and is_white(board.get_tile(forward, x + 1)) != piece_is_white):
            moves.append((forward, x + 1))

        if (x > 0 and board.get_tile(forward, x - 1) is not None
                and is_white(board.get_tile(forward, x - 1)) != piece_is_white):
            moves.append((forward, x - 1))

        if board.get_tile(forward, x) is None:
            moves.append((forward, x))
            # double starting pawn move
            if y == start_pos and board.get_tile(double_y, x) is None:
                moves.append((double_y, x))

    def loop_through_directions(directions: list[pos]) -> None:
        for y_add, x_add in directions:
            for i in range(1, 8):
                new_y = y + i * y_add
                new_x = x + i * x_add
                if not (0 <= new_y < 8 and 0 <= new_x < 8):
                    break
                curr_tile = board.get_tile(new_y, new_x)
                if is_white(curr_tile) == piece_is_white:
                    break
                else:
                    moves.append((new_y, new_x))
                    # hit enemy piece
                    if curr_tile is not None:
                        break

    def rook() -> None:
        # add all moves in 4 direction until hit your or enemy piece
        DIRR = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        loop_through_directions(DIRR)

    def knight() -> None:
        """check all 8 possible knight moves"""
        DIRR = [(2, 0), (-2, 0), (0, 2), (0, -2)]

        for add_y, add_x in DIRR:
            new_y = y + add_y
            new_x = x + add_x

            if not (0 <= new_y < 8 and 0 <= new_x < 8):
                continue

            if add_x == 0:
                if x + 1 < 8 and (board.get_tile(new_y, x + 1) is None or
                                  is_white(board.get_tile(new_y, x + 1)) != piece_is_white):
                    moves.append((new_y, x + 1))

                if x + 1 < 8 and (board.get_tile(new_y, x - 1) is None or
                                  is_white(board.get_tile(new_y, x - 1)) != piece_is_white):
                    moves.append((new_y, x - 1))
            else:
                if y + 1 < 8 and (board.get_tile(y + 1, new_x) is None or
                                  is_white(board.get_tile(y + 1, new_x)) != piece_is_white):
                    moves.append((y + 1, new_x))

                if y - 1 < 8 and (board.get_tile(y - 1, new_x) is None or
                                  is_white(board.get_tile(y - 1, new_x)) != piece_is_white):
                    moves.append((y - 1, new_x))

    # bishop
    def bishop() -> None:
        DIRR = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        loop_through_directions(DIRR)

    # queen
    def queen() -> None:
        rook()
        bishop()

    def king() -> None:
        # castle
        # TODO
        if piece is None:
            pass
            # queen_side_empty_tiles = [(y, 1), (y, 2), (y, 3)]
            # king_side_empty_tiles = [(y, 5), (y, 6)]
            # # rook is in correct position and can castle
            # if (board.get_tile(y, 0).piece == CASLTE_ROOK and board.get_tile(y, 0).colour == piece.colour
            #         and board.range_is_empty(queen_side_empty_tiles)):
            #     moves.append((y, 2))
            # # king side
            # if (board.get_tile(y, 7).piece == CASLTE_ROOK and board.get_tile(y, 7).colour == piece.colour
            #         and board.range_is_empty(king_side_empty_tiles)):
            #     moves.append((y, 6))

        DIRR = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for y_add, x_add in DIRR:
            new_y = y + y_add
            new_x = x + x_add
            if not (0 <= new_y < 8 and 0 <= new_x < 8):
                break
            curr_tile = board.get_tile(new_y, new_x)
            if curr_tile is None or is_white(curr_tile) != piece_is_white:
                moves.append((new_y, new_x))

    list_of_func = [rook, knight, bishop, queen, king, pawn, rook, knight, bishop, queen, king, pawn]
    list_of_func[piece]()
    return moves


def get_block_check_moves(board: Board, curr_pos: pos, moves: list[pos], turn: bool) -> list[pos]:
    # return moves that will block check
    blocking_moves = []
    for new_pos in moves:
        b = copy.copy(board)
        new_b = update_pos(b, curr_pos, new_pos, turn)
        # if not check
        if not is_check(new_b, turn):
            blocking_moves.append(new_pos)
    return blocking_moves


def return_possible_moves(board: Board, piece_cord: pos, turn: bool) -> list[pos]:
    moves = get_piece_moves(board, piece_cord)
    moves = get_block_check_moves(board, piece_cord, moves, turn)
    return moves


def get_all_future_moves(board: Board, turn: bool) -> set[pos]:
    # used only when finding checks
    all_moves = set()
    for y, x in board.get_all_pieces_pos(turn):
        for mov_y, mov_x in get_piece_moves(board, (y, x)):
            all_moves.add((mov_y, mov_x))
    return all_moves


def get_all_moves(board: Board, turn: bool) -> dict[pos, list[pos]]:
    all_moves = {}
    for y, x in board.get_all_pieces_pos(turn):
        all_moves[(y, x)] = return_possible_moves(board, (y, x), turn)
    return all_moves


def is_check(board: Board, turn: bool) -> bool:
    op_turn = not turn
    moves = get_all_future_moves(board, op_turn)

    king_pos = board.get_king_position(turn)
    return king_pos in moves


def update_pos(board: Board, last_cord: pos, wanted_cord: pos, turn: bool) -> Board:
    wanted_y, wanted_x = wanted_cord
    last_y, last_x = last_cord
    curr_piece = board.get_tile(last_y, last_x)

    # if pawn on promotion rank
    if (wanted_y == (7 if turn else 0) and curr_piece == BLACK_PAWN
            or curr_piece == WHITE_PAWN):
        board.replace_tile(last_y, last_x, curr_piece - 2)

    # check castling
    # TODO
    # if curr_piece.piece == CASLTE_KING:
    #     # king side
    #     if wanted_x - last_x == 2:
    #         board.replace_tile(wanted_y, last_x + 1, Tile(curr_piece.colour, ROOK))
    #         board.replace_tile(wanted_y, last_x + 2, Tile(curr_piece.colour, KING))
    #         board.replace_tile(last_y, last_x, Tile())
    #         board.replace_tile(wanted_y, 7, Tile())
    #     # queen side
    #     elif wanted_x - last_x == -2:
    #         board.replace_tile(wanted_y, last_x - 1, Tile(curr_piece.colour, ROOK))
    #         board.replace_tile(wanted_y, last_x - 2, Tile(curr_piece.colour, KING))
    #         board.replace_tile(last_y, last_x, Tile())
    #         board.replace_tile(wanted_y, 0, Tile())
    #     else:
    #         board.move_piece((last_y, last_x), (wanted_y, wanted_x))
    #         # change king id to non castle
    #         board.change_piece(wanted_y, wanted_x, KING)
    board.move_piece((last_y, last_x), (wanted_y, wanted_x))
    # if rook moved change id to non castle
    # if board.get_tile(wanted_y, wanted_x).piece == CASLTE_ROOK:
    #     board.change_piece(wanted_y, wanted_x, ROOK)
    # TODO en passant
    # TODO castling
    # pawn promotion
    return board


def game_over(board: Board, turn: bool) -> bool:
    all_moves = get_all_moves(board, turn)
    for curr_pos, moves in all_moves.items():
        if get_block_check_moves(board, curr_pos, moves, turn):
            return False
    return True
