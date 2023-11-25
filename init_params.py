from constants import *

SX = SCREEN_WIDTH
SY = SCREEN_HEIGHT

INIT_X = np.array((0.0, 1 / 4, 1 / 4, 3 / 4, 3 / 4)) * SX
INIT_Y = np.array((0.0, 1 / 4, 3 / 4, 1 / 4, 3 / 4)) * SY

INIT_VX = np.array((0., 0., -0., 0., -0.)) * 0
INIT_VY = np.array((0., -0., 0., -0., 0.)) * 0

INIT_CLR = np.array((CLR_WHITE, CLR_RED, CLR_BLACK, CLR_BLUE, CLR_WHITE), dtype=np.float16)
INIT_MASS = np.array((1.2, -1.0, -1.0, -1.0, -1.0))                                                      #todo + and - in the same ruin colors
INIT_RAD = np.array((2.0, 2.0, 2.0, 2.0, 2.0))