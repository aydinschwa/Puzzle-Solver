import pygame as pg
import random

pg.init()
pg.display.set_caption("Tangrams")

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

CURR_PIECE_X_OFFSET = 400
CURR_PIECE_Y_OFFSET = 540

LINE_THICKNESS = 5

BACKGROUND = pg.image.load("assets/background.jpg")
