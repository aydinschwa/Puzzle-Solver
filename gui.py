from tangram import TangramSolver
from setup import *
import sys


class TangramGame(TangramSolver):

    def __init__(self):

        super().__init__()

        self.solution = []

        self.board_buffer = [[0, 0, 0, 0, 0, 0, 0, 0].copy() for _ in range(8)]

        self.unused_pieces = [num for num in range(1, 14)]

        self.current_piece = self.pieces[random.choice(self.unused_pieces)]

        self.piece_idx_pointer = 0

        self.game_state = "start"

        self.draw_buffer_event = pg.USEREVENT + 1
        pg.time.set_timer(self.draw_buffer_event, 100)

    #####################################################################
    # Methods for drawing to the screen
    #####################################################################
    def draw_board_outline(self):
        # left
        pg.draw.line(SCREEN, (0, 0, 0),
                     (BOARD_X_OFFSET, BOARD_Y_OFFSET),
                     (BOARD_X_OFFSET, BOARD_Y_OFFSET + len(self.board) * SQUARE_HEIGHT),
                     LINE_THICKNESS)

        # right
        pg.draw.line(SCREEN, (0, 0, 0),
                     (BOARD_X_OFFSET + len(self.board[0]) * SQUARE_WIDTH, BOARD_Y_OFFSET),
                     (BOARD_X_OFFSET + len(self.board[0]) * SQUARE_WIDTH, BOARD_Y_OFFSET + len(self.board) * SQUARE_HEIGHT),
                     LINE_THICKNESS)

        # top
        pg.draw.line(SCREEN, (0, 0, 0),
                     (BOARD_X_OFFSET, BOARD_Y_OFFSET),
                     (BOARD_X_OFFSET + len(self.board[0]) * SQUARE_WIDTH, BOARD_Y_OFFSET),
                     LINE_THICKNESS)

        # bottom
        pg.draw.line(SCREEN, (0, 0, 0),
                     (BOARD_X_OFFSET, BOARD_Y_OFFSET + len(self.board) * SQUARE_HEIGHT),
                     (BOARD_X_OFFSET + len(self.board[0]) * SQUARE_WIDTH, BOARD_Y_OFFSET + len(self.board) * SQUARE_HEIGHT),
                     LINE_THICKNESS)

    @staticmethod
    def draw_title():
        title_word = TITLE_FONT.render("TANGRAMS", True, (0, 0, 0))
        title_rect = title_word.get_rect()
        title_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 10.2)
        SCREEN.blit(title_word, title_rect)

    @staticmethod
    def draw_piece(piece_coords, board, x_offset, y_offset):
        for row, col in piece_coords:
            if board[row][col]:
                pg.draw.rect(SCREEN, COLOR_MAP[board[row][col]], [SQUARE_WIDTH * col + x_offset,
                                                                  SQUARE_HEIGHT * row + y_offset,
                                                                  SQUARE_WIDTH,
                                                                  SQUARE_HEIGHT])

    def draw_buffer(self):
        self.board_buffer = [[0, 0, 0, 0, 0, 0, 0, 0].copy() for _ in range(8)]
        mouse_x, mouse_y = pg.mouse.get_pos()
        row = (mouse_y - BOARD_Y_OFFSET) // SQUARE_HEIGHT
        col = (mouse_x - BOARD_X_OFFSET) // SQUARE_WIDTH
        if (0 <= row < len(self.board)) and (0 <= col < len(self.board[0])):
            legal_moves = self.get_legal_squares(self.board, self.current_piece, False)

            if (row, col) in legal_moves:
                self.board_buffer, _ = self.add_piece(self.board_buffer, self.current_piece, row, col, False)

    def draw_board_pieces(self, board, x_offset, y_offset):
        piece_positions = self.get_piece_positions(board)
        for piece_coord in piece_positions.values():
            self.draw_piece(piece_coord, board, x_offset, y_offset)

    @staticmethod
    def draw_fail_state():
        SCREEN.blit(pg.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        num_iterations_text = NUM_ITERATIONS_FONT.render(f"No Solutions Found!", True, (0, 0, 0))
        num_iterations_rect = num_iterations_text.get_rect()
        num_iterations_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        SCREEN.blit(num_iterations_text, num_iterations_rect)
        pg.display.update()

    def draw_start_state(self):
        SCREEN.blit(pg.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        self.draw_title()
        instructions_text = NUM_ITERATIONS_FONT.render(f"Cycle through pieces with left", True, (0, 0, 0))
        instructions_rect = instructions_text.get_rect()
        instructions_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        SCREEN.blit(instructions_text, instructions_rect)

        instructions_text2 = NUM_ITERATIONS_FONT.render(f"and right arrow keys", True, (0, 0, 0))
        instructions_rect2 = instructions_text2.get_rect()
        instructions_rect2.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3 + 75)
        SCREEN.blit(instructions_text2, instructions_rect2)

        instructions_text3 = NUM_ITERATIONS_FONT.render(f"Rotate and flip with R and F", True, (0, 0, 0))
        instructions_rect3 = instructions_text3.get_rect()
        instructions_rect3.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3 + 150)
        SCREEN.blit(instructions_text3, instructions_rect3)

        instructions_text4 = NUM_ITERATIONS_FONT.render(f"Solve the puzzle with S", True, (0, 0, 0))
        instructions_rect4 = instructions_text4.get_rect()
        instructions_rect4.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3 + 225)
        SCREEN.blit(instructions_text4, instructions_rect4)

        pg.display.update()

    def draw_text(self):
        if self.unused_pieces:
            current_piece_text = NUM_ITERATIONS_FONT.render("Current Piece: ", True, (0, 0, 0))
            current_piece_rect = current_piece_text.get_rect()
            current_piece_rect.center = (SCREEN_WIDTH / 3, SCREEN_HEIGHT / 1.25)
            SCREEN.blit(current_piece_text, current_piece_rect)

        # draw number of iterations if puzzle is solved
        else:
            num_iterations_text = NUM_ITERATIONS_FONT.render(f"Board Positions Searched: {self.iterations:,}", True,
                                                             (0, 0, 0))
            num_iterations_rect = num_iterations_text.get_rect()
            num_iterations_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.3)
            SCREEN.blit(num_iterations_text, num_iterations_rect)

    #####################################################################
    # Methods that access or modify the board state
    #####################################################################
    @staticmethod
    def get_piece_positions(board):
        piece_loc_dict = {num: [] for num in range(1, 14)}
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val:
                    piece_loc_dict[val].append((i, j))
        return piece_loc_dict

    @staticmethod
    def clear_piece(piece_val, board):
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                if val == piece_val:
                    board[i][j] = 0

    def add_erase_piece(self, row, col):
        val = self.board[row][col]
        self.board, legal = self.add_piece(self.board, self.current_piece, row, col, check_islands=False)

        # erase tile unless you're trying to place a piece next to it
        if val and not legal:
            self.clear_piece(val, self.board)
            self.unused_pieces.append(val)

        # place piece if any remain and the move is legal
        elif self.unused_pieces and legal:
            to_remove = None
            for row in self.current_piece:
                for val in row:
                    if val:
                        to_remove = val
                        break
            self.unused_pieces.remove(to_remove)
            if not self.unused_pieces:
                self.solution = self.board
                self.current_piece = [[]]
            else:
                self.current_piece = self.pieces[self.unused_pieces[0]]
            self.piece_idx_pointer = 0

        # special case for when puzzle is solved
        elif not self.unused_pieces:
            self.clear_piece(val, self.board)
            self.unused_pieces.append(val)
            self.current_piece = self.pieces[self.unused_pieces[0]]

    # need to use dumb way of checking islands since can't guarantee that
    # square is the first piece on the board anymore
    @staticmethod
    def check_square(points):
        x_vals = [tup[0] for tup in points]
        y_vals = [tup[1] for tup in points]
        if (max(x_vals) - min(x_vals) == 1) and (max(y_vals) - min(y_vals) == 1):
            return True
        else:
            return False

    def legal_islands(self, board):
        # use bfs to find number of distinct islands
        board = [[elem for elem in row] for row in board]
        board_height = len(board)
        board_width = len(board[0])
        island_cells = []

        def island_bfs(row, col):
            cell_queue = [(row, col)]

            while cell_queue:
                row, col = cell_queue.pop()
                if board[row][col] != 0:
                    continue
                island_cells.append((row, col))
                board[row][col] = "#"
                for row_offset, col_offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    temp_row = row + row_offset
                    temp_col = col + col_offset
                    if 0 <= temp_row < board_height and 0 <= temp_col < board_width and board[temp_row][
                        temp_col] == 0:
                        cell_queue.append((temp_row, temp_col))

        for row in range(board_height):
            for col in range(board_width):
                if board[row][col] == 0:
                    island_bfs(row, col)
                    island_size = len(island_cells)

                    # islands smaller than 4 are illegal
                    if island_size < 4:
                        return False

                    # only allow square shapes for islands of size 4
                    elif island_size == 4:
                        if not self.check_square(island_cells):
                            return False

                    # islands of size 6,7, and 8 are impossible
                    elif island_size in (6, 7, 8):
                        return False

                    island_cells = []
        return True

    def solve_board(self, board, pieces):

        self.iterations += 1

        if self.terminate:
            return

        # win condition is whole board is covered in pieces
        if all([all(row) for row in board]):
            self.draw_board(board)
            self.terminate = True
            self.solution = board
            return
        else:
            piece_positions = pieces[0]
            for position in piece_positions:
                legal_squares = self.get_legal_squares(board, position)
                for row, col in legal_squares:
                    self.solve_board(self.add_piece(board, position, row, col)[0], pieces[1:])

    def display_solution(self):
        unused_pieces = [self.pieces[idx] for idx in self.unused_pieces]
        unused_pieces = self.gen_piece_positions([0] + unused_pieces)

        self.iterations = 0
        self.solution = []
        self.terminate = False
        self.solve_board(self.board, unused_pieces)
        if self.solution:
            self.board = self.solution
            piece_positions = self.get_piece_positions(self.solution)
            for piece_coord in piece_positions.values():
                self.draw_piece(piece_coord, self.board, BOARD_X_OFFSET, BOARD_Y_OFFSET)
                self.draw_board_outline()
                pg.display.update()
                pg.time.wait(250)
            self.unused_pieces = []
            self.current_piece = [[]]

        else:
            self.game_state = "failure"

    #####################################################################
    # Main runner method
    #####################################################################
    def play(self):

        while True:

            # draw background
            SCREEN.blit(pg.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

            # draw failure state if no solutions were found
            if self.game_state == "failure":
                self.draw_fail_state()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.KEYDOWN:
                        self.game_state = "play"
                continue

            elif self.game_state == "start":
                self.draw_start_state()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    if event.type == pg.KEYDOWN:
                        self.game_state = "play"

                continue

            self.draw_title()
            self.draw_text()
            self.draw_board_pieces(self.board, BOARD_X_OFFSET, BOARD_Y_OFFSET)
            self.draw_board_pieces(self.board_buffer, BOARD_X_OFFSET, BOARD_Y_OFFSET)
            self.draw_board_pieces(self.current_piece, CURR_PIECE_X_OFFSET, CURR_PIECE_Y_OFFSET)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                # add or erase tiles from the board with mouse click
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    row = (mouse_y - BOARD_Y_OFFSET) // SQUARE_HEIGHT
                    col = (mouse_x - BOARD_X_OFFSET) // SQUARE_WIDTH
                    if (0 <= row < len(self.board)) and (0 <= col < len(self.board[0])):
                        self.add_erase_piece(row, col)

                if event.type == pg.KEYDOWN and self.unused_pieces:
                    # rotate and flip current piece
                    if event.key == pg.K_r:
                        self.current_piece = self.rotate_piece(self.current_piece)
                    if event.key == pg.K_f:
                        self.current_piece = self.reflect_piece_y(self.current_piece)

                    # cycle through unused pieces
                    if event.key == pg.K_RIGHT or event.key == pg.K_SPACE:
                        self.piece_idx_pointer = (self.piece_idx_pointer + 1) % len(self.unused_pieces)
                        self.current_piece = self.pieces[self.unused_pieces[self.piece_idx_pointer]]

                    if event.key == pg.K_LEFT:
                        self.piece_idx_pointer = (self.piece_idx_pointer - 1) % len(self.unused_pieces)
                        self.current_piece = self.pieces[self.unused_pieces[self.piece_idx_pointer]]

                    # solve puzzle
                    if event.key == pg.K_s:
                        self.display_solution()

                # draw preview of placement of the current tile
                if event.type == self.draw_buffer_event:
                    self.draw_buffer()

            self.draw_board_outline()

            pg.display.update()


if __name__ == "__main__":

    TangramGame().play()
