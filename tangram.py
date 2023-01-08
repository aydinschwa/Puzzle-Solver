

class TangramSolver:

    def __init__(self):

        self.pieces = (

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

        self.color_map = (
            "⬛",
            "⬜",
            "🟥",
            "🟧",
            "🟩",
            "🟦",
            "🟪",
            "🟫",
            "🧿",
            "🌕",
            "👁",
            "🤢",
            "😎",
            "💀"
        )

        self.board = [[0, 0, 0, 0, 0, 0, 0, 0].copy() for _ in range(8)]
        self.pieces = self.gen_piece_positions(self.pieces)

        self.iterations = 0
        self.solutions = 0
        self.terminate = False

    def draw_board(self, board):
        for row in board:
            out_row = []
            for cell in row:
                out_row.append(self.color_map[cell])
            print(" ".join(out_row))
        print()

    @staticmethod
    def rotate_piece(piece):
        return [list(row[::-1]) for row in zip(*piece)]

    def get_rotations(self, piece):
        unique_rotations = [piece]
        for _ in range(3):
            piece = self.rotate_piece(piece)
            if piece not in unique_rotations:
                unique_rotations.append(piece)

        return unique_rotations, len(unique_rotations)

    @staticmethod
    def reflect_piece_x(piece):
        return piece[::-1]

    @staticmethod
    def reflect_piece_y(piece):
        return [row[::-1] for row in piece]

    def get_all_positions(self, piece):
        positions, _ = self.get_rotations(piece)
        for pos in positions:
            y_reflect = self.reflect_piece_y(pos)
            x_reflect = self.reflect_piece_x(pos)
            if y_reflect not in positions:
                positions.append(y_reflect)
            if x_reflect not in positions:
                positions.append(x_reflect)
        return positions

    def gen_piece_positions(self, pieces):
        piece_positions = []
        for piece in pieces[1:]:
            piece_positions.append(self.get_all_positions(piece))
        return piece_positions

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
                island_cells.append((row, col))
                board[row][col] = "#"
                for row_offset, col_offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    temp_row = row + row_offset
                    temp_col = col + col_offset
                    if 0 <= temp_row < board_height and 0 <= temp_col < board_width and board[temp_row][temp_col] == 0:
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
                        if not self.check_square(island_cells.copy()):
                            return False

                    # islands of size 6,7, and 8 are impossible
                    elif island_size in (6, 7, 8):
                        return False

                    island_cells = []
        return True

    def add_piece(self, board, piece, start_row, start_col, check_islands=True):
        piece_width = len(piece[0])
        piece_height = len(piece)
        legal_move = True
        if (start_row + piece_height > len(board)) or (start_col + piece_width > len(board[0])):
            legal_move = False
            return board, legal_move

        changed_squares = []
        for i, row in enumerate(piece):
            for j, val in enumerate(row):
                # only add filled spaces, never take away
                if val != 0:
                    # don't overwrite existing pieces on the board
                    if board[start_row + i][start_col + j] != 0:
                        legal_move = False
                        return board, legal_move
                    else:
                        changed_squares.append((start_row + i, start_col + j, val))

        new_board = [[val for val in row] for row in board]
        for changed_row, changed_col, val in changed_squares:
            new_board[changed_row][changed_col] = val

        # check if the move created any illegal islands
        if check_islands and (not self.legal_islands(new_board)):
            legal_move = False
            return board, legal_move

        return new_board, legal_move

    def get_legal_squares(self, board, piece, check_islands=True):
        legal_moves = []
        for row in range(len(board)):
            for col in range(len(board[0])):
                _, legal_move = self.add_piece(board, piece, row, col, check_islands)
                if legal_move:
                    legal_moves.append((row, col))
        return legal_moves

    def solve_board(self, board, pieces):

        self.iterations += 1

        if self.terminate:
            return

        # win condition is whole board is covered in pieces
        if all([all(row) for row in board]):
            self.solutions += 1
            print(f"Solutions: {self.solutions}")
            print(self.iterations)
            self.draw_board(board)
            return board
        else:
            piece_positions = pieces[0]
            for position in piece_positions:
                legal_squares = self.get_legal_squares(board, position)
                for row, col in legal_squares:
                    self.solve_board(self.add_piece(board, position, row, col)[0], pieces[1:])

    def run(self):
        self.solve_board(self.board, self.pieces)


if __name__ == "__main__":

    TangramSolver().run()
