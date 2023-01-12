from tangram import TangramSolver
from collections import defaultdict
import pickle


# pull the piece we want off the board so we can compare it to the template piece
def extract_piece(board, piece_val):
    col_max_idx = 0
    col_min_idx = 100
    piece = []
    for i, row in enumerate(board):
        if piece_val in row:
            col_max_idx, col_min_idx = max(col_max_idx, len(row) - row[::-1].index(piece_val)), \
                                       min(col_min_idx, row.index(piece_val))

            piece.append([elem if elem == piece_val else 0 for elem in row])

    piece = [row[col_min_idx:col_max_idx] for row in piece]
    return piece


# returns how many flips and rotations are needed to change piece orientation to its template
def assimilate_pieces(base, variant):
    def check_equal(piece1, piece2):
        for v1, v2 in zip(piece1, piece2):
            if v1 != v2:
                return False
        return True

    rotations = 0
    while True:
        if check_equal(base, variant):
            return rotations, False

        variant = reflect_piece_y(variant)

        if check_equal(base, variant):
            return rotations, True

        variant = reflect_piece_y(variant)

        variant = rotate_piece(variant)
        rotations += 1


# flip/rotate board until chosen piece is in the correct configuration
def shift_board(board, rotations, flip):
    for _ in range(rotations):
        board = rotate_piece(board)

    if flip:
        board = reflect_piece_y(board)
    return board


def standardize_board(board):
    piece_val = 10
    template = TangramSolver().pieces[piece_val]
    piece = extract_piece(board, piece_val)
    num_rotations, to_flip = assimilate_pieces(template, piece)
    board = shift_board(board, num_rotations, to_flip)
    return board


def find_unique_solutions(solutions):
    solution_dict = defaultdict(int)
    num_solutions = len(solutions)
    for i, solution in enumerate(solutions):
        if i % 10_000 == 0:
            print(f"{i:,} solutions checked out of {num_solutions:,} total")

        standard_solution = standardize_board(solution)

        # ah yes premium hash
        position_hash = str(standard_solution)
        solution_dict[position_hash] += 1

    print(f"There are {len(solution_dict):,} unique solutions to the block tangram puzzle")

    unique_sols = [eval(solution) for solution in solution_dict.keys()]
    return unique_sols


if __name__ == "__main__":
    # load solutions file
    FileStore = open("solutions/solutions_duplicates.pickle", "rb")
    solutions = pickle.load(FileStore)
    FileStore.close()

    # grab functions we need from TangramSolver
    rotate_piece = TangramSolver.rotate_piece
    reflect_piece_y = TangramSolver.reflect_piece_y

    unique_solutions = find_unique_solutions(solutions)

    # save unique solutions
    FileStore = open("solutions/solutions_unique.pickle", "wb")
    pickle.dump(unique_solutions, FileStore)
    FileStore.close()
