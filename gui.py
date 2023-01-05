import pygame as pg
from tangram import *
from setup import *
import sys


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

    game_state = "play"

    global BOARD
    global BOARD_BUFFER
    global CURRENT_PIECE
    global UNUSED_PIECES
    piece_idx_pointer = 0

    global iterations
    global solution
    global terminate

    DRAW_BUFFER = pg.USEREVENT + 1
    pg.time.set_timer(DRAW_BUFFER, 100)

    while True:

        # draw background
        SCREEN.blit(pg.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        if game_state != "play":
            SCREEN.blit(pg.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
            num_iterations_text = NUM_ITERATIONS_FONT.render(f"No Solutions Found!", True, (0, 0, 0))
            num_iterations_rect = num_iterations_text.get_rect()
            num_iterations_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            SCREEN.blit(num_iterations_text, num_iterations_rect)
            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    game_state = "play"

            continue

        # draw title
        title_word = TITLE_FONT.render("TANGRAMS", True, (0, 0, 0))
        title_rect = title_word.get_rect()
        title_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 10.2)
        SCREEN.blit(title_word, title_rect)

        # draw "current piece"
        if UNUSED_PIECES:
            current_piece_text = NUM_ITERATIONS_FONT.render("Current Piece: ", True, (0, 0, 0))
            current_piece_rect = current_piece_text.get_rect()
            current_piece_rect.center = (SCREEN_WIDTH / 5, SCREEN_HEIGHT / 1.25)
            SCREEN.blit(current_piece_text, current_piece_rect)

        # draw number of iterations
        if not UNUSED_PIECES:
            num_iterations_text = NUM_ITERATIONS_FONT.render(f"Board Positions Searched: {iterations}", True, (0, 0, 0))
            num_iterations_rect = num_iterations_text.get_rect()
            num_iterations_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.3)
            SCREEN.blit(num_iterations_text, num_iterations_rect)

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
                        if not UNUSED_PIECES:
                            solution = BOARD
                            CURRENT_PIECE = [[]]
                        else:
                            CURRENT_PIECE = PIECES[UNUSED_PIECES[0]]
                        piece_idx_pointer = 0

                    # special case for when puzzle is solved
                    elif not UNUSED_PIECES:
                        clear_piece(val, BOARD)
                        UNUSED_PIECES.append(val)
                        CURRENT_PIECE = PIECES[UNUSED_PIECES[0]]

            if event.type == pg.KEYDOWN:

                # rotate and flip current piece
                if event.key == pg.K_r:
                    CURRENT_PIECE = rotate_piece(CURRENT_PIECE)
                if event.key == pg.K_f:
                    CURRENT_PIECE = reflect_piece_y(CURRENT_PIECE)

                # cycle through unused pieces
                if event.key == pg.K_RIGHT or event.key == pg.K_SPACE:
                    piece_idx_pointer = (piece_idx_pointer + 1) % len(UNUSED_PIECES)
                    CURRENT_PIECE = PIECES[UNUSED_PIECES[piece_idx_pointer]]

                if event.key == pg.K_LEFT:
                    piece_idx_pointer = (piece_idx_pointer - 1) % len(UNUSED_PIECES)
                    CURRENT_PIECE = PIECES[UNUSED_PIECES[piece_idx_pointer]]

                # solve puzzle
                if event.key == pg.K_s:
                    unused_pieces = [PIECES[idx] for idx in UNUSED_PIECES]
                    unused_pieces = gen_piece_positions([0] + unused_pieces)

                    iterations = 0
                    solution = []
                    terminate = False
                    solve_board(BOARD, unused_pieces)
                    if solution:
                        BOARD = solution
                        piece_positions = get_piece_positions(solution)
                        for piece_coord in piece_positions.values():
                            draw_piece(piece_coord, BOARD, BOARD_X_OFFSET, BOARD_Y_OFFSET)
                            draw_board_outline()
                            pg.display.update()
                            pg.time.wait(250)
                        UNUSED_PIECES = []
                        CURRENT_PIECE = [[]]

                    else:
                        game_state = "fail"

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

        draw_board_outline()

        pg.display.update()


if __name__ == "__main__":
    iterations = 0
    solution = []
    terminate = False
    main()
