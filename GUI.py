import pygame

pygame.init()

# load images
bg = pygame.image.load("assets\\board.png")

bishopB = pygame.image.load("assets\\pieces\\BishopB.png")
bishopW = pygame.image.load("assets\\pieces\\BishopW.png")
kingB = pygame.image.load("assets\\pieces\\KingB.png")
kingW = pygame.image.load("assets\\pieces\\KingW.png")
knightB = pygame.image.load("assets\\pieces\\KnightB.png")
knightW = pygame.image.load("assets\\pieces\\KnightW.png")
pawnB = pygame.image.load("assets\\pieces\\PawnB.png")
pawnW = pygame.image.load("assets\\pieces\\PawnW.png")
queenB = pygame.image.load("assets\\pieces\\QueenB.png")
queenW = pygame.image.load("assets\\pieces\\QueenW.png")
rookB = pygame.image.load("assets\\pieces\\RookB.png")
rookW = pygame.image.load("assets\\pieces\\RookW.png")


##################################################################################
board = pygame.display.set_mode((1200, 800))

# create grid (y,x )


def move_pieces(piece, position):
    pass


def create_pices():
    pass


def grid():
    # grid start 82, 86 size 80*80
    start_x = 82
    start_y = 86
    pcs_size = 80
    grid = []
    for y in range(8):
        for x in range(8):
            grid.append([start_x + (pcs_size*x), start_y+(pcs_size*y)])

            # test
            pygame.draw.rect(board, (255, 0, 0), (start_x +
                                                  (pcs_size*x), start_y+(pcs_size*y), 80, 80), 1)


def display_update():
    board.blit(bg, (0, 0))
    grid()

    pygame.display.update()
