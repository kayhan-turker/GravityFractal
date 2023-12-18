from constants import *


INIT_X = np.array((0.0, 0.0, 1.0, 0.0, 1.0)) * SCREEN_WIDTH
INIT_Y = np.array((0.0, 0.0, 1.0, 1.0, 0.0)) * SCREEN_HEIGHT

INIT_VX = np.array((0., 0., 0., 0., 0.)) * 0
INIT_VY = np.array((0., 0., 0., 0., 0.)) * 0

INIT_CLR = np.array((CLR_WHITE, CLR_YELLOW, CLR_BLUE, CLR_GREEN, CLR_PINK), dtype=np.float16)
INIT_RAD = np.array((1.0, 1.0, 1.0, 1.0, 1.0)) * 2.0
INIT_MASS = np.array((1.0, 1.0, 1.0, 1.0, 1.0)) * 4 / 3 * PI * INIT_RAD * INIT_RAD * INIT_RAD              # todo + and - in the same ruin colors

INIT_FREE = np.array((1, 0, 0, 0, 0), dtype=bool)
