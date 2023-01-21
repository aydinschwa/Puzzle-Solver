# Puzzle-Solver

This repo contains both an interactive pentomino puzzle and a built-in solver. The solver uses backtracking to explore all possible board configurations until it encounters a solution. You'll have to download Pygame if you want to play with the interactive solver, but otherwise vanilla Python is all you need.
</br>
</br>

<p align="center">
  <img src="images/solutions.gif" width="300" height="300"/>
</p>

# File Structure
gui.py -> interactive pentomino puzzle

tangram.py -> main body of the actual solver, cleanest implementation

tangram_multi.py -> inherits from tangram.py, uses Python's multiprocessing library to speed up the simulation

remove_duplicates.py -> checks a list of solved boards for duplicates

setup.py -> parameters for gui.py

solutions -> contains a pickle file with all 16,146 unique solutions to the puzzle
