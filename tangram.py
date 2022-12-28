import copy


def draw_board(board):
    for row in board:
        out_row = []
        for cell in row:
            if cell == 1:
                out_row.append("⬜")
            elif cell == 0:
                out_row.append("⬛")
        print(" ".join(out_row))
    print()


def add_piece(board, piece, start_row, start_col, draw=False):
    piece_width = len(piece[0])
    piece_height = len(piece)
    legal_move = True
    new_board = copy.deepcopy(board)
    if (start_row + piece_height > len(board)) or (start_col + piece_width > len(board[0])):
        legal_move = False
        return board, legal_move
    for i, row in enumerate(piece):
        for j, val in enumerate(row):
            # only add filled spaces, never take away
            if val == 1:
                # don't overwrite existing pieces on the board
                if board[start_row + i][start_col + j] == 1:
                    legal_move = False
                    return board, legal_move
                else:
                    new_board[start_row + i][start_col + j] = val
    if draw:
        draw_board(new_board)
    return new_board, legal_move


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


def get_legal_squares(board, piece):
    legal_moves = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            _, legal_move = add_piece(board, piece, row, col)
            if legal_move:
                legal_moves.append((row, col))
    return legal_moves


pieces = {

    "ladder": [[1, 1, 0],
               [0, 1, 1],
               [0, 0, 1]],

    "right angle": [[1, 0, 0],
                    [1, 0, 0],
                    [1, 1, 1]],

    "plus": [[0, 1, 0],
             [1, 1, 1],
             [0, 1, 0]],

    "long": [[1, 1, 1, 1, 1]],

    "big L": [[1, 0],
              [1, 0],
              [1, 0],
              [1, 1]],

    "square": [[1, 1],
               [1, 1]],

    "T": [[1, 1, 1],
          [0, 1, 0],
          [0, 1, 0]],

    "arch": [[1, 1, 1],
             [1, 0, 1]],

    "house": [[1, 0],
              [1, 1],
              [1, 1]],

    "twist": [[1, 1, 0],
              [0, 1, 1],
              [0, 1, 0]],

    "tree": [[1, 0],
             [1, 1],
             [0, 1],
             [0, 1]],

    "arm": [[1, 0],
            [1, 1],
            [1, 0],
            [1, 0]],

    "S": [[1, 1, 0],
          [0, 1, 0],
          [0, 1, 1]]
}

sub_pieces = {
    "tree": [[1, 0],
             [1, 1],
             [0, 1],
             [0, 1]],

    "arm": [[1, 0],
            [1, 1],
            [1, 0],
            [1, 0]],

    "T": [[1, 1, 1],
          [0, 1, 0],
          [0, 1, 0]],

    "right angle": [[1, 0, 0],
                    [1, 0, 0],
                    [1, 1, 1]]
}


def test_positions():
    for name, piece in pieces.items():
        positions = get_all_positions(piece)
        print(name, len(positions))


full_board = [[0, 0, 0, 0, 0, 0, 0, 0].copy() for _ in range(8)]
half_board = [[0, 0, 0, 0, 0].copy() for _ in range(4)]
pieces = gen_piece_positions(pieces)
pieces = gen_piece_positions(sub_pieces)


def solve_board(board, pieces):
    # win condition is whole board is covered in pieces
    draw_board(board)
    if all([all(row) for row in board]):
        draw_board(board)
        return board
    else:
        piece_positions = pieces[0]
        for position in piece_positions:
            legal_squares = get_legal_squares(board, position)
            for row, col in legal_squares:
                solve_board(add_piece(board, position, row, col)[0], pieces[1:])


solve_board(half_board, list(pieces.values()))

# for name, group in pieces.items():
#     print(name)
#     [draw_board(piece) for piece in group]
#     print()

# print(pieces)

