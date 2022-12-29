

#########################################################
# Project: Pygame tangram interface that finds solutions
# for arbitrary tangram configurations
#########################################################

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
              [0,  10, 10],
              [0,  10, 0]],

    "tree": [[11, 0],
             [11, 11],
             [0,  11],
             [0,  11]],

    "arm": [[12, 0],
            [12, 12],
            [12, 0],
            [12, 0]],

    "S": [[13, 13, 0],
          [0,  13, 0],
          [0,  13, 13]]
}


color_map = (
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


def draw_board(board):
    for row in board:
        out_row = []
        for cell in row:
            out_row.append(color_map[cell])
        print(" ".join(out_row))
    print()


def rotate_piece(piece):
    return [list(row[::-1]) for row in zip(*piece)]


def get_rotations(piece):
    unique_rotations = [piece]
    for _ in range(3):
        piece = rotate_piece(piece)
        if piece not in unique_rotations:
            unique_rotations.append(piece)

    return unique_rotations, len(unique_rotations)


def reflect_piece_x(piece):
    return piece[::-1]


def reflect_piece_y(piece):
    return [row[::-1] for row in piece]


def get_all_positions(piece):
    positions, _ = get_rotations(piece)
    for pos in positions:
        y_reflect = reflect_piece_y(pos)
        x_reflect = reflect_piece_x(pos)
        if y_reflect not in positions:
            positions.append(y_reflect)
        if x_reflect not in positions:
            positions.append(x_reflect)
    return positions


def gen_piece_positions(pieces):
    piece_positions = {}
    for name, piece in pieces.items():
        piece_positions[name] = get_all_positions(piece)
    return piece_positions


def check_square(points):
    x_vals = [tup[0] for tup in points]
    y_vals = [tup[1] for tup in points]
    if (max(x_vals) - min(x_vals) == 1) and (max(y_vals) - min(y_vals) == 1):
        return True
    else:
        return False


# use bfs to find number of distinct islands
def legal_islands(board):
    board = [[elem for elem in row] for row in board]
    board_height = len(board)
    board_width = len(board[0])
    island_cells = []

    def island_bfs(row, col):
        cell_queue = [(row, col)]
        if row < 0 or col < 0 or row >= board_height or col >= board_width or board[row][col] != 0:
            pass
        while cell_queue:
            row, col = cell_queue.pop()
            island_cells.append((row, col))
            board[row][col] = "#"
            if row > 0 and board[row - 1][col] == 0:
                cell_queue.append((row - 1, col))
            if col > 0 and board[row][col - 1] == 0:
                cell_queue.append((row, col - 1))
            if row < board_height - 1 and board[row + 1][col] == 0:
                cell_queue.append((row + 1, col))
            if col < board_width - 1 and board[row][col + 1] == 0:
                cell_queue.append((row, col + 1))

    for row in range(board_height):
        for col in range(board_width):
            if board[row][col] == 0:
                island_bfs(row, col)
                island_size = len(island_cells)

                if island_size < 4:
                    return False
                elif island_size == 4:
                    if not check_square(island_cells):
                        return False
                elif island_size in (6, 7, 8):
                    return False
                island_cells = []
    return True


def add_piece(board, piece, start_row, start_col):
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
    if not legal_islands(new_board):
        legal_move = False
        return board, legal_move

    return new_board, legal_move


def get_legal_squares(board, piece):
    legal_moves = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            _, legal_move = add_piece(board, piece, row, col)
            if legal_move:
                legal_moves.append((row, col))
    return legal_moves


def solve_board(board, pieces):

    global iterations
    global terminate

    iterations += 1
    # if iterations % 20000 == 0:
    #     terminate = True

    if terminate:
        return

    # win condition is whole board is covered in pieces
    if all([all(row) for row in board]):
        print(iterations)
        print(board)
        draw_board(board)
        return board
    else:
        piece_positions = pieces[0]
        for position in piece_positions:
            legal_squares = get_legal_squares(board, position)
            for row, col in legal_squares:
                solve_board(add_piece(board, position, row, col)[0], pieces[1:])


full_board = [[0, 0, 0, 0, 0, 0, 0, 0].copy() for _ in range(8)]
half_board = [[0, 0, 0, 0, 0].copy() for _ in range(4)]
pieces = gen_piece_positions(pieces)

iterations = 0
terminate = False

if __name__ == "__main__":
    solve_board(full_board, list(pieces.values()))
