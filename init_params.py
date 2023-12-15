from constants import *

SX = SCREEN_WIDTH
SY = SCREEN_HEIGHT

INIT_X = np.array((0.0, 0.2, 0.8, 0.2, 0.8)) * SX
INIT_Y = np.array((0.0, 0.2, 0.8, 0.8, 0.2)) * SY

INIT_VX = np.array((0., 0., 0., 0., 0.)) * 0
INIT_VY = np.array((0., 0., 0., 0., 0.)) * 0

INIT_CLR = np.array((CLR_WHITE, CLR_WHITE, CLR_BLACK, CLR_BLACK, CLR_WHITE), dtype=np.float16)
INIT_MASS = np.array((2.0, 2.0, -1.0, -1.0, 2.0)) * 1.0                                  # todo + and - in the same ruin colors
INIT_RAD = np.array((1.0, 1.0, 1.0, 1.0, 1.0)) * 1.0

INIT_FREE = np.array((1, 1, 1, 1, 1), dtype=bool)
