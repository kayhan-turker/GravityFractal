
import numpy as np

GRID_LENGTH = 1
SCREEN_WIDTH = 960 - GRID_LENGTH
SCREEN_HEIGHT = 960 - GRID_LENGTH

NUM_COLS = SCREEN_WIDTH // GRID_LENGTH
NUM_ROWS = SCREEN_HEIGHT // GRID_LENGTH

GRAV_CONST = 1
WALL_COLLISION = True
SIM_SPEED = 1

MIN_GRID_DISPLAY_LENGTH = 4

PIXEL_TRANSPARENCY = 2.0
PIXEL_TIME_CONTRAST = 0.05
PIXEL_HIT_TRANSPARENCY = np.array([1.0, 0.4, 0.2, 0.1])
MAX_PIXEL_HITS = len(PIXEL_HIT_TRANSPARENCY)

PIXEL_BACK_CLR = np.array((128, 128, 128))

CLR_WHITE = np.array((1.0, 1.0, 1.0), dtype=np.float16) * 255
CLR_BLACK = np.array((0.0, 0.0, 0.0), dtype=np.float16) * 255
CLR_GREY = np.array((0.5, 0.5, 0.5), dtype=np.float16) * 255

CLR_RED = np.array((1.0, 0.1, 0.4), dtype=np.float16) * 255
CLR_YELLOW = np.array((1.0, 0.9, 0.4), dtype=np.float16) * 255
CLR_GREEN = np.array((0.0, 1.0, 0.6), dtype=np.float16) * 255
CLR_BLUE = np.array((0.0, 0.4, 1.0), dtype=np.float16) * 255
CLR_PURPLE = np.array((0.7, 0.2, 1.0), dtype=np.float16) * 255
