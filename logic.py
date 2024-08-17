import copy

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

    def restart_board(self) -> None:
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

    def get_tile(self, y: int, x: int) -> Tile:
        bit_index = get_bit_index((y, x))
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

        new_bit_mask = 1 << get_bit_index(new_cord)
        old_bit_mask = 1 << get_bit_index(old_cord)

        self.board[piece] ^= old_bit_mask
        if removed_piece is not None:
            self.board[removed_piece] ^= new_bit_mask
        self.board[piece] |= new_bit_mask

        return removed_piece

    def remove_piece(self, cord: pos) -> Tile:
        y, x = cord
        piece = self.get_tile(y, x)
        assert piece is not None

        bit_mask = 1 << get_bit_index(cord)
        self.board[piece] ^= bit_mask
        return piece

    def change_piece(self, cord: pos, new_piece: Tile) -> None:
        assert new_piece is not None
        y, x = cord
        curr_piece = self.get_tile(y, x)
        assert curr_piece is not None

        bit_mask = 1 << get_bit_index(cord)
        self.board[curr_piece] ^= bit_mask
        self.board[new_piece] |= bit_mask

    def tile_is_empty(self, y: int, x: int) -> bool:
        return self.get_tile(y, x) is None

    def range_is_empty(self, rng: list[pos]) -> bool:
        for y, x in rng:
            if not self.tile_is_empty(y, x):
                return False
        return True

    def get_all_pieces_pos(self, color: bool | None = None) -> list[pos]:
        """get coordinates of every piece"""
        pieces: list[pos] = []
        board_sum = self.get_bit_sum(color)
        for i in range(8 * 8):
            bit_mask = 1 << i
            if (board_sum & bit_mask) != 0:
                pieces.append(get_coordinates(i))
        return pieces

    def get_king_position(self, white_turn: bool) -> pos:
        king = WHITE_KING if white_turn else BLACK_KING
        for i in range(8 * 8):
            bit_mask = 1 << i
            if (self.board[king] & bit_mask) != 0:
                return get_coordinates(i)
        assert False


class ChessGame:

    def __init__(self) -> None:
        self.board = Board()
        # [ white king side, white queen side, ....]
        self.castle_rights = [False for _ in range(4)]
        # use to record enemy double pawn move for en passant
        self.double_pawn_move: None | pos = None

        self.white_turn = True
        self.check = False
        self.checkmate = False

        self.restart_game()

    def restart_game(self) -> None:
        self.board.restart_board()
        self.castle_rights = [True for _ in range(4)]
        self.double_pawn_move = None
        self.white_turn = True
        self.check = False
        self.checkmate = False

    def can_castle(self, white_turn: bool, king_side: bool) -> bool:
        index = 0 if white_turn else 2
        index += 0 if king_side else 1
        return self.castle_rights[index]

    def remove_castle_right(self, white_turn: bool, king_side: bool) -> None:
        index = 0 if white_turn else 2
        index += 0 if king_side else 1
        self.castle_rights[index] = False

    def get_piece_moves(self, piece_cord: pos) -> list[pos]:
        """return all possible moves for piece"""
        y, x = piece_cord
        piece = self.board.get_tile(y, x)
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
            if (x < 7 and self.board.get_tile(forward, x + 1) is not None
                    and is_white(self.board.get_tile(forward, x + 1)) != piece_is_white):
                moves.append((forward, x + 1))

            if (x > 0 and self.board.get_tile(forward, x - 1) is not None
                    and is_white(self.board.get_tile(forward, x - 1)) != piece_is_white):
                moves.append((forward, x - 1))

            if self.board.get_tile(forward, x) is None:
                moves.append((forward, x))
                # double starting pawn move
                if y == start_pos and self.board.get_tile(double_y, x) is None:
                    moves.append((double_y, x))

            # en passant
            if self.double_pawn_move is not None:
                if self.double_pawn_move == (y, x - 1):
                    moves.append((forward, x - 1))
                elif self.double_pawn_move == (y, x + 1):
                    moves.append((forward, x + 1))

        def loop_through_directions(directions: list[pos]) -> None:
            for y_add, x_add in directions:
                for i in range(1, 8):
                    new_y = y + i * y_add
                    new_x = x + i * x_add
                    if not (0 <= new_y < 8 and 0 <= new_x < 8):
                        break
                    curr_tile = self.board.get_tile(new_y, new_x)
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
                curr_tile = self.board.get_tile(new_y, new_x)
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
            if self.can_castle(piece_is_white, True) and self.board.range_is_empty(king_side_empty_tiles):
                moves.append((y, 6))
            # queen side
            if self.can_castle(piece_is_white, False) and self.board.range_is_empty(queen_side_empty_tiles):
                moves.append((y, 2))

            DIRR = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

            for y_add, x_add in DIRR:
                new_y = y + y_add
                new_x = x + x_add
                if not (0 <= new_y < 8 and 0 <= new_x < 8):
                    continue
                curr_tile = self.board.get_tile(new_y, new_x)
                if curr_tile is None or not is_same_color(curr_tile, piece):
                    moves.append((new_y, new_x))

        list_of_func = [pawn, rook, knight, bishop, queen, king, pawn, rook, knight, bishop, queen, king]
        list_of_func[piece]()
        return moves

    def return_possible_moves(self, piece_cord: pos) -> list[pos]:
        moves = self.get_piece_moves(piece_cord)
        return self.get_block_check_moves(piece_cord, moves)

    def get_all_future_moves(self, turn: bool) -> set[pos]:
        # used only when finding checks
        all_moves = set()
        for y, x in self.board.get_all_pieces_pos(turn):
            for mov_y, mov_x in self.get_piece_moves((y, x)):
                all_moves.add((mov_y, mov_x))
        return all_moves

    def get_all_moves(self) -> dict[pos, list[pos]]:
        all_moves = {}
        for y, x in self.board.get_all_pieces_pos(self.white_turn):
            all_moves[(y, x)] = self.return_possible_moves((y, x))
        return all_moves

    def is_check(self) -> bool:
        op_turn = not self.white_turn
        moves = self.get_all_future_moves(op_turn)

        king_pos = self.board.get_king_position(self.white_turn)
        return king_pos in moves

    def is_checkmate(self) -> bool:
        all_moves = self.get_all_moves()
        for curr_pos, moves in all_moves.items():
            if self.get_block_check_moves(curr_pos, moves):
                return False
        return True

    def get_block_check_moves(self, curr_pos: pos, moves: list[pos]) -> list[pos]:
        # return moves that will block check
        blocking_moves = []
        for new_pos in moves:
            b = copy.deepcopy(self)
            b.update_pos(curr_pos, new_pos)
            # if not check
            if not b.is_check():
                blocking_moves.append(new_pos)
        return blocking_moves

    def update_pos(self, last_cord: pos, wanted_cord: pos) -> None:
        wanted_y, wanted_x = wanted_cord
        last_y, last_x = last_cord
        curr_piece = self.board.get_tile(last_y, last_x)

        self.double_pawn_move = None

        if curr_piece == BLACK_PAWN or curr_piece == WHITE_PAWN:
            # pawn promotion
            # TODO
            if wanted_y == (0 if self.white_turn else 7):
                promote_to = WHITE_QUEEN if self.white_turn else BLACK_QUEEN
                self.board.change_piece(last_cord, promote_to)
            # en passant
            if wanted_x != last_x and wanted_y != last_y and self.board.tile_is_empty(wanted_y, wanted_x):
                below = 1 if self.white_turn else -1
                self.board.remove_piece((wanted_y + below, wanted_x))
            # record double pawn move
            elif abs(wanted_y - last_y) == 2:
                self.double_pawn_move = (wanted_y, wanted_x)

        self.board.move_piece((last_y, last_x), (wanted_y, wanted_x))

        # castling
        if curr_piece == WHITE_KING or curr_piece == BLACK_KING:
            # king side
            if self.can_castle(self.white_turn, True) and wanted_x - last_x == 2:
                self.board.move_piece((last_y, 7), (last_y, 5))
            # queen side
            elif self.can_castle(self.white_turn, False) and wanted_x - last_x == -2:
                self.board.move_piece((last_y, 0), (last_y, 2))

            self.remove_castle_right(self.white_turn, True)
            self.remove_castle_right(self.white_turn, False)

        if curr_piece == BLACK_ROOK or curr_piece == WHITE_ROOK:
            # queen side
            if last_x == 0:
                self.remove_castle_right(self.white_turn, False)
            # king side
            elif last_x == 7:
                self.remove_castle_right(self.white_turn, True)

    def make_move(self, last_cord: pos, wanted_cord: pos) -> None:
        # valid move
        assert wanted_cord in self.get_all_moves()[last_cord]
        self.update_pos(last_cord, wanted_cord)
        self.white_turn = not self.white_turn
        self.check = self.is_check()
        self.checkmate = self.is_checkmate()


def is_white(tile: Tile) -> bool:
    return tile is not None and tile > BLACK_KING


def is_same_color(t1: Tile, t2: Tile) -> bool:
    return t1 is not None and t2 is not None and is_white(t1) == is_white(t2)


def get_bit_index(coordinates: pos) -> int:
    y, x = coordinates
    return 63 - (y * 8 + x)


def get_coordinates(bit_index: int) -> pos:
    y = 7 - (bit_index // 8)
    x = 7 - (bit_index % 8)
    return y, x
