from tangram import TangramSolver
import pickle
import multiprocessing


class MultiSolver(TangramSolver):

    def __init__(self, process_num):
        super().__init__()
        self.process_num = process_num

    def get_legal_squares(self, board, piece, check_islands=True):
        legal_moves = []
        for row in range(len(board)):
            for col in range(len(board[0])):
                if piece[0][0] == 1 and row != self.process_num:
                    break
                _, legal_move = self.add_piece(board, piece, row, col, check_islands)
                if legal_move:
                    legal_moves.append((row, col))
        return legal_moves

    def solve_board(self, board, pieces, save_results=False):

        self.iterations += 1

        if (self.iterations % 10_000_000 == 0) and save_results:
            FileStore = open(f"stored_objects/solutions_duplicates_{self.process_num}.pickle", "wb")
            pickle.dump(self.solutions, FileStore)
            FileStore.close()

        if self.terminate:
            return

        # win condition is whole board is covered in pieces
        if all([all(row) for row in board]):
            self.solutions.append(board)
            print(f"Process Number: {self.process_num}")
            print(f"Solutions: {len(self.solutions):,}")
            print(f"Iterations: {self.iterations:,}\n")
            return board
        else:
            piece_positions = pieces[0]
            for position in piece_positions:
                legal_squares = self.get_legal_squares(board, position)
                for row, col in legal_squares:
                    self.solve_board(self.add_piece(board, position, row, col)[0], pieces[1:], save_results)

    def run(self, save_results=False):
        self.solve_board(self.board, self.piece_positions, save_results)

        if save_results:
            FileStore = open(f"stored_objects/solutions_duplicates_{self.process_num}.pickle", "wb")
            pickle.dump(self.solutions, FileStore)
            FileStore.close()


def multi_sim(process_num):
    MultiSolver(process_num).run(save_results=False)


if __name__ == "__main__":
    processes = []
    for i in range(7):
        p = multiprocessing.Process(target=multi_sim, args=(i,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    # combine all solutions after all processes finish running
    solutions = []
    for i in range(7):
        FileStore = open(f"stored_objects/solutions_duplicates_{i}.pickle", "rb")
        row_solutions = pickle.load(FileStore)
        FileStore.close()
        solutions.extend(row_solutions)

    FileStore = open("solutions/combined.pickle", "wb")
    pickle.dump(solutions, FileStore)
    FileStore.close()
