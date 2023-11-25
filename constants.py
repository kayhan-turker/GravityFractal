
import numpy as np

GRID_LENGTH = 16
SCREEN_WIDTH = 720 - GRID_LENGTH
SCREEN_HEIGHT = 720 - GRID_LENGTH

NUM_COLS = SCREEN_WIDTH // GRID_LENGTH
NUM_ROWS = SCREEN_HEIGHT // GRID_LENGTH

GRAV_CONST = 1
WALL_COLLISION = True
SIM_SPEED = 2

MIN_GRID_DISPLAY_LENGTH = 4

PIXEL_TRANSPARENCY = 1.0
PIXEL_TIME_CONTRAST = 0.1

SOLID_CLR = 0.5
PIXEL_BACK_CLR = np.array((SOLID_CLR, SOLID_CLR, SOLID_CLR), dtype=np.float16) * 255

CLR_WHITE = np.array((1.0, 1.0, 1.0), dtype=np.float16) * 255
CLR_BLACK = np.array((0.0, 0.0, 0.0), dtype=np.float16) * 255
CLR_GREY = np.array((0.5, 0.5, 0.5), dtype=np.float16) * 255

CLR_RED = np.array((1.0, 0.1, 0.4), dtype=np.float16) * 255
CLR_YELLOW = np.array((1.0, 0.9, 0.4), dtype=np.float16) * 255
CLR_GREEN = np.array((0.0, 1.0, 0.6), dtype=np.float16) * 255
CLR_BLUE = np.array((0.0, 0.4, 1.0), dtype=np.float16) * 255
CLR_PURPLE = np.array((0.7, 0.2, 1.0), dtype=np.float16) * 255
