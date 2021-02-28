
import GUI


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

    def __init__(self, piece, color, restart_position):
        self.piece = piece
        self.color = color
        self.restart_position = restart_position

    def gui_call(self):
        pass

    def gui_restart(self):
        GUI.create_pices(self.piece, self.color, self.restart_position)

    def pawn_rules(self):
        pass


white_pieces = []


def restart_pieces():
    global white_pieces, black_pieces
    white_pieces = [playing_pieces(0, 0, (0, 6)),
                    playing_pieces(0, 0, (1, 6)),
                    playing_pieces(0, 0, (2, 6)),
                    playing_pieces(0, 0, (3, 6)),
                    playing_pieces(0, 0, (4, 6)),
                    playing_pieces(0, 0, (5, 6)),
                    playing_pieces(0, 0, (6, 6)),
                    playing_pieces(0, 0, (7, 6)),

                    playing_pieces(1, 0, (0, 7)),
                    playing_pieces(2, 0, (1, 7)),
                    playing_pieces(3, 0, (2, 7)),
                    playing_pieces(4, 0, (3, 7)),
                    playing_pieces(5, 0, (4, 7)),
                    playing_pieces(3, 0, (5, 7)),
                    playing_pieces(2, 0, (6, 7)),
                    playing_pieces(1, 0, (7, 7)),
                    ]
    black_pieces = [playing_pieces(0, 1, (0, 1)),
                    playing_pieces(0, 1, (1, 1)),
                    playing_pieces(0, 1, (2, 1)),
                    playing_pieces(0, 1, (3, 1)),
                    playing_pieces(0, 1, (4, 1)),
                    playing_pieces(0, 1, (5, 1)),
                    playing_pieces(0, 1, (6, 1)),
                    playing_pieces(0, 1, (7, 1)),

                    playing_pieces(1, 1, (0, 0)),
                    playing_pieces(2, 1, (1, 0)),
                    playing_pieces(3, 1, (2, 0)),
                    playing_pieces(4, 1, (3, 0)),
                    playing_pieces(5, 1, (4, 0)),
                    playing_pieces(3, 1, (5, 0)),
                    playing_pieces(2, 1, (6, 0)),
                    playing_pieces(1, 1, (7, 0)),

                    ]
    for pcs in white_pieces:
        pcs.gui_restart()
    for bpcs in black_pieces:
        bpcs.gui_restart()
