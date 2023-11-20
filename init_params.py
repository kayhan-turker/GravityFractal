import numpy as np
from constants import *

SX = SCREEN_WIDTH
SY = SCREEN_HEIGHT

INIT_X = np.array((0.0, SX * 1 / 3, SX * 2 / 3))
INIT_Y = np.array((0.0, SY / 2, SY / 2))

INIT_VX = np.array((0.0, 0.0, 0.0))
INIT_VY = np.array((0.0, 0.0, -0.0))

INIT_CLR = np.array(((255, 255, 255), (255, 0, 0), (0, 0, 255)))
INIT_MASS = np.array((0.0, 0.0, 1.0))
INIT_RAD = np.array((2.0, 8.0, 8.0))
