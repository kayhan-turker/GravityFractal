import numpy as np

GRID_LENGTH = 3
SCREEN_WIDTH = 480 - GRID_LENGTH
SCREEN_HEIGHT = 480 - GRID_LENGTH

NUM_COLS = SCREEN_WIDTH // GRID_LENGTH
NUM_ROWS = SCREEN_HEIGHT // GRID_LENGTH

GRAV_CONST = 1.0
WALL_COLLISION = True
SIM_SPEED = 0.1

GRAV_MATRIX_MODE = False
GRAV_MATRIX = np.array([[0, 1, 1, 1, 1],
                        [0, 0, -1, 0, 1],
                        [0, 1, 0, -1, 0],
                        [0, 0, 1, 0, -1],
                        [0, -1, 0, 1, 0]], dtype=np.float16) * GRAV_CONST

# 0 = average, 1 = linear, 2 = cubic
RADIUS_ADDITION_MODE = 2

TIMELAPSE_ENABLED = True
TIMELAPSE_FRAMES = 20
IMG_SAVE_PATH = "out/"

MIN_GRID_DISPLAY_LENGTH = 4

# == PIXEL COLOR SETTINGS ====================================== #

PIXEL_BACK_CLR = np.array((128, 128, 128))

# 0 = object decided, 1 = angle decided
HUE_MODE = 0
# 0 = time decided, 1 = speed decided
VALUE_MODE = 0

START_PIXEL_TRANSPARENCY = 1.0
PIXEL_TIME_CONTRAST = 0.1
MASS_WEIGHTED_TRANSPARENCY = False
PIXEL_HIT_TRANSPARENCY = np.array([1.0, 0.5, 0.25, 0.125])

MAX_PIXEL_HITS = len(PIXEL_HIT_TRANSPARENCY)

# == COLOR CONSTANTS =========================================== #

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