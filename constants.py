
import numpy as np

GRID_LENGTH = 4
SCREEN_WIDTH = 480 - GRID_LENGTH
SCREEN_HEIGHT = 480 - GRID_LENGTH

NUM_COLS = SCREEN_WIDTH // GRID_LENGTH
NUM_ROWS = SCREEN_HEIGHT // GRID_LENGTH

GRAV_CONST = 1
WALL_COLLISION = True
SIM_SPEED = 1

MIN_GRID_DISPLAY_LENGTH = 4

PIXEL_TRANSPARENCY = 4.0
PIXEL_TIME_CONTRAST = 0.1
MASS_TRANSPARENCY = True
PIXEL_HIT_TRANSPARENCY = np.array([1.0, 0.5])
MAX_PIXEL_HITS = len(PIXEL_HIT_TRANSPARENCY)

PIXEL_BACK_CLR = np.array((150, 150, 150))

CLR_WHITE = np.array((1.0, 1.0, 1.0), dtype=np.float16) * 255
CLR_BLACK = np.array((0.0, 0.0, 0.0), dtype=np.float16) * 255
CLR_GREY = np.array((0.5, 0.5, 0.5), dtype=np.float16) * 255

CLR_RED = np.array((0.8, 0.36, 0.36), dtype=np.float16) * 255
CLR_YELLOW = np.array((0.8, 0.73, 0.36), dtype=np.float16) * 255
CLR_GREEN = np.array((0.36, 0.8, 0.51), dtype=np.float16) * 255
CLR_BLUE = np.array((0.36, 0.43, 0.8), dtype=np.float16) * 255
CLR_PURPLE = np.array((0.7, 0.2, 1.0), dtype=np.float16) * 255
CLR_PINK = np.array((0.8, 0.36, 0.65), dtype=np.float16) * 255

PRIM_RED = np.array((1.0, 0.0, 0.0), dtype=np.float16) * 255
PRIM_YELLOW = np.array((1.0, 1.0, 0.0), dtype=np.float16) * 255
PRIM_GREEN = np.array((0.0, 1.0, 0.0), dtype=np.float16) * 255
PRIM_BLUE = np.array((0.0, 0.0, 1.0), dtype=np.float16) * 255

CLR_PAL_RED = np.array((0.93, 0.17, 0.21), dtype=np.float16) * 255
CLR_PAL_GREEN = np.array((0.0, 0.59, 0.21), dtype=np.float16) * 255