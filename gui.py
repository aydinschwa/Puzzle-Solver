import pygame as pg
from tangram import rotate_piece, reflect_piece_y, gen_piece_positions, get_legal_squares, add_piece, draw_board
import sys

pieces = (

    [],

    [[1, 1, 0],
     [0, 1, 1],
     [0, 0, 1]],

    [[2, 0, 0],
     [2, 0, 0],
     [2, 2, 2]],

    [[0, 3, 0],
     [3, 3, 3],
     [0, 3, 0]],

    [[4, 4, 4, 4, 4]],

    [[5, 0],
     [5, 0],
     [5, 0],
     [5, 5]],

    [[6, 6],
     [6, 6]],

    [[7, 7, 7],
     [0, 7, 0],
     [0, 7, 0]],

    [[8, 8, 8],
     [8, 0, 8]],

    [[9, 0],
     [9, 9],
     [9, 9]],

    [[10, 10, 0],
     [0, 10, 10],
     [0, 10, 0]],

    [[11, 0],
     [11, 11],
     [0, 11],
     [0, 11]],

    [[12, 0],
     [12, 12],
     [12, 0],
     [12, 0]],

    [[13, 13, 0],
     [0, 13, 0],
     [0, 13, 13]]
)

BOARD = [[1, 1, 7, 7, 7, 2, 6, 6],
         [12, 1, 1, 7, 11, 2, 6, 6],
         [12, 12, 1, 7, 11, 2, 2, 2],
         [12, 13, 13, 11, 11, 3, 8, 8],
         [12, 13, 0, 11, 3, 3, 3, 8],
         [13, 13, 0, 0, 0, 3, 8, 8],
         [9, 9, 9, 0, 5, 5, 5, 5],
         [9, 9, 4, 4, 4, 4, 4, 5]]

BOARD_BUFFER = [[0, 0, 0, 0, 0, 0, 0, 0].copy() for _ in range(8)]


BANK = [[1, 1, 0, 7, 7, 7, 0, 2, 0, 6, 6],
        [12, 0, 1, 1, 0, 7, 0, 11, 0, 2, 0, 6, 6],
        ]

COLOR_MAP = {
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

CURRENT_PIECE = reflect_piece_y(rotate_piece(pieces[10]))

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

SQUARE_WIDTH = 50
SQUARE_HEIGHT = 50
SQUARE_MARGIN = 2

BOARD_X_OFFSET = 50
BOARD_Y_OFFSET = 150

BANK_X_OFFSET = 500
BANK_Y_OFFSET = 150

BACKGROUND = pg.image.load("assets/background.jpg")


def get_piece_positions(board):
    piece_loc_dict = {num: [] for num in range(1, 14)}
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val != 0:
                piece_loc_dict[val].append((i, j))

    return piece_loc_dict


def draw_piece(piece_coords, board, x_offset, y_offset, alpha=0):
    for row, col in piece_coords:
        if board[row][col]:
            pg.draw.rect(SCREEN, COLOR_MAP[board[row][col]], [SQUARE_WIDTH * col + x_offset,
                                                              SQUARE_HEIGHT * row + y_offset,
                                                              SQUARE_WIDTH,
                                                              SQUARE_HEIGHT])


# def draw_piece(piece_coords, board, x_offset, y_offset, alpha=1):
#     for row, col in piece_coords:
#         if board[row][col]:
#             pg.draw.rect(SCREEN, COLOR_MAP[board[row][col]], [SQUARE_WIDTH * col + x_offset,
#                                                               SQUARE_HEIGHT * row + y_offset,
#                                                               SQUARE_WIDTH,
#                                                               SQUARE_HEIGHT])


def clear_piece(piece_val, board):
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == piece_val:
                board[i][j] = 0


def main():
    pg.init()
    pg.display.set_caption("Tangrams")

    global BOARD
    global BOARD_BUFFER
    global CURRENT_PIECE

    DRAW_BUFFER = pg.USEREVENT + 1
    pg.time.set_timer(DRAW_BUFFER, 100)

    while True:
        SCREEN.blit(pg.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # add or erase tiles from the board with mouse click
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                row = (mouse_y - BOARD_Y_OFFSET) // SQUARE_HEIGHT
                col = (mouse_x - BOARD_X_OFFSET) // SQUARE_WIDTH
                val = BOARD[row][col]
                if val:
                    clear_piece(val, BOARD)
                else:
                    BOARD, _ = add_piece(BOARD, CURRENT_PIECE, row, col)
                    CURRENT_PIECE = [[]]

            # draw preview of placement of the current tile
            if event.type == DRAW_BUFFER:
                BOARD_BUFFER = [[0, 0, 0, 0, 0, 0, 0, 0].copy() for _ in range(8)]
                mouse_x, mouse_y = pg.mouse.get_pos()
                row = (mouse_y - BOARD_Y_OFFSET) // SQUARE_HEIGHT
                col = (mouse_x - BOARD_X_OFFSET) // SQUARE_WIDTH
                if (0 <= row < len(BOARD)) and (0 <= col < len(BOARD[0])):
                    val = BOARD[row][col]
                    legal_moves = get_legal_squares(BOARD, CURRENT_PIECE, False)

                    if (row, col) in legal_moves:
                        BOARD_BUFFER, _ = add_piece(BOARD_BUFFER, CURRENT_PIECE, row, col, False)

        # draw board and buffer pieces
        piece_positions = get_piece_positions(BOARD)
        for piece_coord in piece_positions.values():
            draw_piece(piece_coord, BOARD, BOARD_X_OFFSET, BOARD_Y_OFFSET)

        # draw buffer pieces
        piece_positions = get_piece_positions(BOARD_BUFFER)
        for piece_coord in piece_positions.values():
            draw_piece(piece_coord, BOARD_BUFFER, BOARD_X_OFFSET, BOARD_Y_OFFSET, 1)

        pg.display.update()


if __name__ == "__main__":

    main()
