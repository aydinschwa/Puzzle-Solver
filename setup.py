import pygame as pg
import random

pg.init()
pg.display.set_caption("Tangrams")

PIECES = (

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

COLOR_MAP = (
    (),
    (0, 0, 0),
    (255, 255, 255),
    (0, 255, 255),
    (0, 0, 255),
    (255, 0, 255),
    (255, 255, 0),
    (128, 128, 128),
    (255, 0, 0),
    (0, 255, 0),
    (45, 170, 45),
    (128, 0, 255),
    (255, 128, 0),
    (128, 0, 0)
)

BOARD = [[0, 0, 0, 0, 0, 0, 0, 0].copy() for _ in range(8)]

BOARD_BUFFER = [[0, 0, 0, 0, 0, 0, 0, 0].copy() for _ in range(8)]

UNUSED_PIECES = [num for num in range(1, 14)]

CURRENT_PIECE = PIECES[random.choice(UNUSED_PIECES)]

TITLE_FONT = pg.font.Font("assets/OstrichSans-Black.otf", 100)
NUM_ITERATIONS_FONT = pg.font.Font("assets/OstrichSans-Black.otf", 50)
CURRENT_PIECE_FONT = pg.font.Font("assets/ostrich-regular.ttf", 50)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

SQUARE_WIDTH = 50
SQUARE_HEIGHT = 50
SQUARE_MARGIN = 2

BOARD_X_OFFSET = 145
BOARD_Y_OFFSET = 120

CURR_PIECE_X_OFFSET = 280
CURR_PIECE_Y_OFFSET = 540

LINE_THICKNESS = 5

BACKGROUND = pg.image.load("assets/background.jpg")
