from constants import *

SX = SCREEN_WIDTH
SY = SCREEN_HEIGHT

INIT_X = np.array((0.0, 1.35 / 4, 1.35 / 4, 2.65 / 4, 2.65 / 4)) * SX
INIT_Y = np.array((0.0, 1.35 / 4, 2.65 / 4, 1.35 / 4, 2.65 / 4)) * SY

INIT_VX = np.array((0., 0., -0., 0., -0.)) * 0
INIT_VY = np.array((0., -0., 0., -0., 0.)) * 0

INIT_CLR = np.array((CLR_WHITE, CLR_PINK, CLR_YELLOW, CLR_BLUE, CLR_GREEN), dtype=np.float16)
INIT_MASS = np.array((1.2, -1.0, -1.0, -1.0, -1.0))                  * -1                                     #todo + and - in the same ruin colors
INIT_RAD = np.array((2.0, 2.0, 2.0, 2.0, 2.0))

INIT_FREE = np.array((1, 1, 1, 1, 1), dtype=bool)
