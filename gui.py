import pygame as pg
import sys


pieces = {

    "ladder": [[1, 1, 0],
               [0, 1, 1],
               [0, 0, 1]],

    "right angle": [[2, 0, 0],
                    [2, 0, 0],
                    [2, 2, 2]],

    "plus": [[0, 3, 0],
             [3, 3, 3],
             [0, 3, 0]],

    "long": [[4, 4, 4, 4, 4]],

    "big L": [[5, 0],
              [5, 0],
              [5, 0],
              [5, 5]],

    "square": [[6, 6],
               [6, 6]],

    "T": [[7, 7, 7],
          [0, 7, 0],
          [0, 7, 0]],

    "arch": [[8, 8, 8],
             [8, 0, 8]],

    "house": [[9, 0],
              [9, 9],
              [9, 9]],

    "twist": [[10, 10, 0],
              [0, 10, 10],
              [0, 10, 0]],

    "tree": [[11, 0],
             [11, 11],
             [0, 11],
             [0, 11]],

    "arm": [[12, 0],
            [12, 12],
            [12, 0],
            [12, 0]],

    "S": [[13, 13, 0],
          [0, 13, 0],
          [0, 13, 13]]
}

board = [[1, 1, 7, 7, 7, 2, 6, 6],
         [12, 1, 1, 7, 11, 2, 6, 6],
         [12, 12, 1, 7, 11, 2, 2, 2],
         [12, 13, 13, 11, 11, 3, 8, 8],
         [12, 13, 0, 11, 3, 3, 3, 8],
         [13, 13, 0, 0, 0, 3, 8, 8],
         [9, 9, 9, 0, 5, 5, 5, 5],
         [9, 9, 4, 4, 4, 4, 4, 5]]

color_map = {
    1: (0, 0, 0),
    2: (255, 255, 255),
    3: (0, 255, 255),
    4: (0, 0, 255),
    5: (255, 0, 255),
    6: (255, 255, 0),
    7: (128, 128, 128),
    8: (255, 0, 0),
    9: (0, 255, 0),
    10: (45, 170, 45),
    11: (128, 0, 255),
    12: (255, 128, 0),
    13: (128, 0, 0)
}


def get_piece_positions(board):
    piece_loc_dict = {num: [] for num in range(1, 14)}
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val != 0:
                piece_loc_dict[val].append((i, j))

    return piece_loc_dict


SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

SQUARE_WIDTH = 50
SQUARE_HEIGHT = 50
SQUARE_MARGIN = 2

SQUARE_X_OFFSET = 50
SQUARE_Y_OFFSET = 150

BACKGROUND = pg.image.load("assets/background.jpg")


def draw_piece(piece_coords):
    for row, col in piece_coords:
        if board[row][col]:
            pg.draw.rect(SCREEN, color_map[board[row][col]], [SQUARE_WIDTH * row + SQUARE_X_OFFSET,
                                                              SQUARE_HEIGHT * col + SQUARE_Y_OFFSET,
                                                              SQUARE_WIDTH,
                                                              SQUARE_HEIGHT])


def main():
    pg.init()
    pg.display.set_caption("Tangrams")

    while True:
        SCREEN.blit(pg.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        piece_positions = get_piece_positions(board)
        for piece_coord in piece_positions.values():
            draw_piece(piece_coord)

        pg.display.update()


if __name__ == "__main__":
    full_board = [[0, 0, 0, 0, 0, 0, 0, 0].copy() for _ in range(8)]
    main()
