from constants import *

SX = SCREEN_WIDTH
SY = SCREEN_HEIGHT

INIT_X = np.array((0.0, SX * 1 / 2 + 40, SX * 1 / 2, SX * 1 / 2 - 40, SX * 1 / 2))
INIT_Y = np.array((0.0, SY * 1 / 2, SY * 1 / 2 + 40, SY * 1 / 2, SY * 1 / 2 - 40))

INIT_VX = np.array((0.0, 0.5, -0.5, 0.0, -0.0)) * 0
INIT_VY = np.array((0.0, -0.5, 0.5, -0.0, 0.0)) * 0

INIT_CLR = np.array(((255, 255, 255), (180, 64, 64), (54, 125, 200), (180, 64, 64), (54, 125, 200)),
                    dtype=np.float16)
INIT_MASS = np.array((10.0, 10.0, 10.0, 10.0, 10.0))
INIT_RAD = np.array((2.0, 2.0, 2.0, 2.0, 2.0))