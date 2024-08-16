import copy
import enum

BLACK_PAWN = 0
BLACK_ROOK = 1
BLACK_KNIGHT = 2
BLACK_BISHOP = 3
BLACK_QUEEN = 4
BLACK_KING = 5
WHITE_PAWN = 6
WHITE_ROOK = 7
WHITE_KNIGHT = 8
WHITE_BISHOP = 9
WHITE_QUEEN = 10
WHITE_KING = 11

Tile = int | None
pos = tuple[int, int]


class Board:
    """
    Represent board using 12 numbers
    Each number represent 64 bits of information
    Each number encode position of 1 type of piece
    """

    def __init__(self) -> None:
        self.board = [0 for _ in range(12)]
        # [ white king side, white queen side, ....]
        self.castle_rights = [False for _ in range(4)]
        # use to record enemy double pawn move for en passant
        self.double_pawn_move: None | pos = None
        self.restart_board()

    def restart_board(self) -> None:
        self.castle_rights = [True for _ in range(4)]
        self.double_pawn_move = None

        self.board[BLACK_PAWN] = 0b0000000011111111000000000000000000000000000000000000000000000000
        self.board[BLACK_ROOK] = 0b1000000100000000000000000000000000000000000000000000000000000000
        self.board[BLACK_KNIGHT] = 0b0100001000000000000000000000000000000000000000000000000000000000
        self.board[BLACK_BISHOP] = 0b0010010000000000000000000000000000000000000000000000000000000000
        self.board[BLACK_QUEEN] = 0b0001000000000000000000000000000000000000000000000000000000000000
        self.board[BLACK_KING] = 0b0000100000000000000000000000000000000000000000000000000000000000

        self.board[WHITE_PAWN] = 0b1111111100000000
        self.board[WHITE_ROOK] = 0b10000001
        self.board[WHITE_KNIGHT] = 0b01000010
        self.board[WHITE_BISHOP] = 0b00100100
        self.board[WHITE_QUEEN] = 0b00010000
        self.board[WHITE_KING] = 0b00001000

    def get_bit_sum(self, color: bool | None = None) -> int:
        result = 0
        start = WHITE_PAWN if color is True else 0
        end = WHITE_PAWN if color is False else 12
        for i in range(start, end):
            result |= self.board[i]
        return result

    def get_bit_index(self, coordinates: pos) -> int:
        y, x = coordinates
        return 63 - (y * 8 + x)

    def get_coordinates(self, bit_index: int) -> pos:
        y = 7 - (bit_index // 8)
        x = 7 - (bit_index % 8)
        return y, x

    def get_tile(self, y: int, x: int) -> Tile:
        bit_index = self.get_bit_index((y, x))
        bit_mask = 1 << bit_index
        for i in range(12):
            if (self.board[i] & bit_mask) != 0:
                return i
        return None

    def move_piece(self, old_cord: pos, new_cord: pos) -> Tile:
        new_y, new_x = new_cord
        old_y, old_x = old_cord

        piece = self.get_tile(old_y, old_x)
        assert piece is not None
        removed_piece = self.get_tile(new_y, new_x)

        new_bit_mask = 1 << self.get_bit_index(new_cord)
        old_bit_mask = 1 << self.get_bit_index(old_cord)

        self.board[piece] ^= old_bit_mask
        if removed_piece is not None:
            self.board[removed_piece] ^= new_bit_mask
        self.board[piece] |= new_bit_mask

        return removed_piece

    def remove_piece(self, cord: pos) -> Tile:
        y, x = cord
        piece = self.get_tile(y, x)
        assert piece is not None

        bit_mask = 1 << self.get_bit_index(cord)
        self.board[piece] ^= bit_mask
        return piece

    def change_piece(self, cord: pos, new_piece: Tile) -> None:
        assert new_piece is not None
        y, x = cord
        curr_piece = self.get_tile(y, x)
        assert curr_piece is not None

        bit_mask = 1 << self.get_bit_index(cord)
        self.board[curr_piece] ^= bit_mask
        self.board[new_piece] |= bit_mask

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

    def get_king_position(self, white: bool) -> pos:
        king = WHITE_KING if white else BLACK_KING
        for i in range(8 * 8):
            bit_mask = 1 << i
            if (self.board[king] & bit_mask) != 0:
                return self.get_coordinates(i)
        assert False

    def can_castle(self, white_turn: bool, king_side: bool) -> bool:
        index = 0 if white_turn else 2
        index += 0 if king_side else 1
        return self.castle_rights[index]

    def remove_castle_right(self, white_turn: bool, king_side: bool) -> None:
        index = 0 if white_turn else 2
        index += 0 if king_side else 1
        self.castle_rights[index] = False


def is_white(tile: Tile) -> bool:
    return tile is not None and tile > BLACK_KING


def is_same_color(t1: Tile, t2: Tile) -> bool:
    return t1 is not None and t2 is not None and is_white(t1) == is_white(t2)


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

        # en passant
        if board.double_pawn_move is not None:
            if board.double_pawn_move == (y, x - 1):
                moves.append((forward, x - 1))
            elif board.double_pawn_move == (y, x + 1):
                moves.append((forward, x + 1))

    def loop_through_directions(directions: list[pos]) -> None:
        for y_add, x_add in directions:
            for i in range(1, 8):
                new_y = y + i * y_add
                new_x = x + i * x_add
                if not (0 <= new_y < 8 and 0 <= new_x < 8):
                    break
                curr_tile = board.get_tile(new_y, new_x)
                if is_same_color(curr_tile, piece):
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
        DIRR = [(2, 1), (-2, 1), (1, 2), (1, -2),
                (2, -1), (-2, -1), (-1, 2), (-1, -2)]

        for y_add, x_add in DIRR:
            new_y = y + y_add
            new_x = x + x_add
            if not (0 <= new_y < 8 and 0 <= new_x < 8):
                continue
            curr_tile = board.get_tile(new_y, new_x)
            if curr_tile is None or not is_same_color(curr_tile, piece):
                moves.append((new_y, new_x))

    def bishop() -> None:
        DIRR = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        loop_through_directions(DIRR)

    def queen() -> None:
        rook()
        bishop()

    def king() -> None:
        king_side_empty_tiles = [(y, 5), (y, 6)]
        queen_side_empty_tiles = [(y, 1), (y, 2), (y, 3)]

        # king side castle
        if board.can_castle(piece_is_white, True) and board.range_is_empty(king_side_empty_tiles):
            moves.append((y, 6))
        # queen side
        if board.can_castle(piece_is_white, False) and board.range_is_empty(queen_side_empty_tiles):
            moves.append((y, 2))

        DIRR = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for y_add, x_add in DIRR:
            new_y = y + y_add
            new_x = x + x_add
            if not (0 <= new_y < 8 and 0 <= new_x < 8):
                continue
            curr_tile = board.get_tile(new_y, new_x)
            if curr_tile is None or not is_same_color(curr_tile, piece):
                moves.append((new_y, new_x))

    list_of_func = [pawn, rook, knight, bishop, queen, king, pawn, rook, knight, bishop, queen, king]
    list_of_func[piece]()
    return moves


def get_block_check_moves(board: Board, curr_pos: pos, moves: list[pos], turn: bool) -> list[pos]:
    # return moves that will block check
    blocking_moves = []
    for new_pos in moves:
        b = copy.deepcopy(board)
        new_b = update_pos(b, curr_pos, new_pos, turn)
        # if not check
        if not is_check(new_b, turn):
            blocking_moves.append(new_pos)
    return blocking_moves


def return_possible_moves(board: Board, piece_cord: pos, turn: bool) -> list[pos]:
    moves = get_piece_moves(board, piece_cord)
    return get_block_check_moves(board, piece_cord, moves, turn)


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

    board.double_pawn_move = None

    if curr_piece == BLACK_PAWN or curr_piece == WHITE_PAWN:
        # pawn promotion
        # TODO
        if wanted_y == (0 if turn else 7):
            promote_to = WHITE_QUEEN if turn else BLACK_QUEEN
            board.change_piece(last_cord, promote_to)
        # en passant
        if wanted_x != last_x and wanted_y != last_y and board.tile_is_empty(wanted_y, wanted_x):
            below = 1 if turn else -1
            board.remove_piece((wanted_y + below, wanted_x))
        # record double pawn move
        elif abs(wanted_y - last_y) == 2:
            board.double_pawn_move = (wanted_y, wanted_x)

    board.move_piece((last_y, last_x), (wanted_y, wanted_x))

    # castling
    if curr_piece == WHITE_KING or curr_piece == BLACK_KING:
        # king side
        if board.can_castle(turn, True) and wanted_x - last_x == 2:
            board.move_piece((last_y, 7), (last_y, 5))
        # queen side
        elif board.can_castle(turn, False) and wanted_x - last_x == -2:
            board.move_piece((last_y, 0), (last_y, 2))

        board.remove_castle_right(turn, True)
        board.remove_castle_right(turn, False)

    if curr_piece == BLACK_ROOK or curr_piece == WHITE_ROOK:
        # queen side
        if last_x == 0:
            board.remove_castle_right(turn, False)
        # king side
        elif last_x == 7:
            board.remove_castle_right(turn, True)

    return board


def game_over(board: Board, turn: bool) -> bool:
    all_moves = get_all_moves(board, turn)
    for curr_pos, moves in all_moves.items():
        if get_block_check_moves(board, curr_pos, moves, turn):
            return False
    return True
