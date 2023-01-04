import pygame as pg
from tangram import *
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

BOARD = [[0, 0, 0, 0, 0, 0, 0, 0].copy() for _ in range(8)]
BOARD_BUFFER = [[0, 0, 0, 0, 0, 0, 0, 0].copy() for _ in range(8)]


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
# UNUSED_PIECES = [10]
UNUSED_PIECES = [num for num in range(1, 14)]

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

SQUARE_WIDTH = 50
SQUARE_HEIGHT = 50
SQUARE_MARGIN = 2

BOARD_X_OFFSET = 145
BOARD_Y_OFFSET = 120

CURR_PIECE_X_OFFSET = 260
CURR_PIECE_Y_OFFSET = 540

LINE_THICKNESS = 5

BACKGROUND = pg.image.load("assets/background.jpg")

iterations = 0
solutions = None
terminate = False


def get_piece_positions(board):
    piece_loc_dict = {num: [] for num in range(1, 14)}
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val != 0:
                piece_loc_dict[val].append((i, j))

    return piece_loc_dict


def draw_piece(piece_coords, board, x_offset, y_offset):
    for row, col in piece_coords:
        if board[row][col]:
            pg.draw.rect(SCREEN, COLOR_MAP[board[row][col]], [SQUARE_WIDTH * col + x_offset,
                                                              SQUARE_HEIGHT * row + y_offset,
                                                              SQUARE_WIDTH,
                                                              SQUARE_HEIGHT])


def clear_piece(piece_val, board):
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == piece_val:
                board[i][j] = 0


def draw_board_outline():
    # left
    pg.draw.line(SCREEN, (0, 0, 0),
                 (BOARD_X_OFFSET, BOARD_Y_OFFSET),
                 (BOARD_X_OFFSET, BOARD_Y_OFFSET + len(BOARD) * SQUARE_HEIGHT),
                 LINE_THICKNESS)

    # right
    pg.draw.line(SCREEN, (0, 0, 0),
                 (BOARD_X_OFFSET + len(BOARD[0]) * SQUARE_WIDTH, BOARD_Y_OFFSET),
                 (BOARD_X_OFFSET + len(BOARD[0]) * SQUARE_WIDTH, BOARD_Y_OFFSET + len(BOARD) * SQUARE_HEIGHT),
                 LINE_THICKNESS)

    # top
    pg.draw.line(SCREEN, (0, 0, 0),
                 (BOARD_X_OFFSET, BOARD_Y_OFFSET),
                 (BOARD_X_OFFSET + len(BOARD[0]) * SQUARE_WIDTH, BOARD_Y_OFFSET),
                 LINE_THICKNESS)

    # bottom
    pg.draw.line(SCREEN, (0, 0, 0),
                 (BOARD_X_OFFSET, BOARD_Y_OFFSET + len(BOARD) * SQUARE_HEIGHT),
                 (BOARD_X_OFFSET + len(BOARD[0]) * SQUARE_WIDTH, BOARD_Y_OFFSET + len(BOARD) * SQUARE_HEIGHT),
                 LINE_THICKNESS)


def solve_board(board, pieces):

    global iterations
    global solution
    global terminate

    iterations += 1

    if terminate:
        return

    # win condition is whole board is covered in pieces
    if all([all(row) for row in board]):
        draw_board(board)
        terminate = True
        solution = board
        return
    else:
        piece_positions = pieces[0]
        for position in piece_positions:
            legal_squares = get_legal_squares(board, position)
            for row, col in legal_squares:
                solve_board(add_piece(board, position, row, col)[0], pieces[1:])


def main():
    pg.init()
    pg.display.set_caption("Tangrams")

    global BOARD
    global BOARD_BUFFER
    global CURRENT_PIECE
    global UNUSED_PIECES
    piece_idx_pointer = 0

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
                if (0 <= row < len(BOARD)) and (0 <= col < len(BOARD[0])):
                    val = BOARD[row][col]
                    BOARD, legal = add_piece(BOARD, CURRENT_PIECE, row, col, check_islands=False)

                    # erase tile unless you're trying to place a piece next to it
                    if val and not legal:
                        clear_piece(val, BOARD)
                        UNUSED_PIECES.append(val)

                    # place piece if any remain and the move is legal
                    elif UNUSED_PIECES and legal:
                        to_remove = None
                        for row in CURRENT_PIECE:
                            for val in row:
                                if val:
                                    to_remove = val
                                    break
                        UNUSED_PIECES.remove(to_remove)
                        CURRENT_PIECE = pieces[UNUSED_PIECES[0]]
                        piece_idx_pointer = 0

            if event.type == pg.KEYDOWN:

                # rotate and flip current piece
                if event.key == pg.K_r:
                    CURRENT_PIECE = rotate_piece(CURRENT_PIECE)
                if event.key == pg.K_f:
                    CURRENT_PIECE = reflect_piece_y(CURRENT_PIECE)

                # cycle through unused pieces
                if event.key == pg.K_RIGHT or event.key == pg.K_SPACE:
                    piece_idx_pointer = (piece_idx_pointer + 1) % len(UNUSED_PIECES)
                    CURRENT_PIECE = pieces[UNUSED_PIECES[piece_idx_pointer]]

                if event.key == pg.K_LEFT:
                    piece_idx_pointer = (piece_idx_pointer - 1) % len(UNUSED_PIECES)
                    CURRENT_PIECE = pieces[UNUSED_PIECES[piece_idx_pointer]]

                # solve puzzle
                if event.key == pg.K_s:
                    unused_pieces = [pieces[idx] for idx in UNUSED_PIECES]
                    unused_pieces = gen_piece_positions([0] + unused_pieces)
                    global iterations
                    global solution
                    global terminate
                    iterations = 0
                    solution = None
                    terminate = False
                    solve_board(BOARD, unused_pieces)
                    if solution:
                        print(solution)
                    else:
                        print("No solutions found!")

            # draw preview of placement of the current tile
            if event.type == DRAW_BUFFER:
                BOARD_BUFFER = [[0, 0, 0, 0, 0, 0, 0, 0].copy() for _ in range(8)]
                mouse_x, mouse_y = pg.mouse.get_pos()
                row = (mouse_y - BOARD_Y_OFFSET) // SQUARE_HEIGHT
                col = (mouse_x - BOARD_X_OFFSET) // SQUARE_WIDTH
                if (0 <= row < len(BOARD)) and (0 <= col < len(BOARD[0])):
                    legal_moves = get_legal_squares(BOARD, CURRENT_PIECE, False)

                    if (row, col) in legal_moves:
                        BOARD_BUFFER, _ = add_piece(BOARD_BUFFER, CURRENT_PIECE, row, col, False)

        # draw board pieces
        piece_positions = get_piece_positions(BOARD)
        for piece_coord in piece_positions.values():
            draw_piece(piece_coord, BOARD, BOARD_X_OFFSET, BOARD_Y_OFFSET)

        # draw buffer pieces
        piece_positions = get_piece_positions(BOARD_BUFFER)
        for piece_coord in piece_positions.values():
            draw_piece(piece_coord, BOARD_BUFFER, BOARD_X_OFFSET, BOARD_Y_OFFSET)

        # draw current piece
        piece_positions = get_piece_positions(CURRENT_PIECE)
        for piece_coord in piece_positions.values():
            draw_piece(piece_coord, CURRENT_PIECE, CURR_PIECE_X_OFFSET, CURR_PIECE_Y_OFFSET)

        draw_board_outline()

        pg.display.update()


if __name__ == "__main__":
    main()
