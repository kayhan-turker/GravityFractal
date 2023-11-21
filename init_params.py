import numpy as np
from constants import *

SX = SCREEN_WIDTH
SY = SCREEN_HEIGHT

INIT_X = np.array((0.0, 0., 0., SX, SX))
INIT_Y = np.array((0.0, 0., SY, SY, 0.))

INIT_VX = np.array((0.0, 0.0, 0.1, 0.0, -0.1))
INIT_VY = np.array((0.0, 0.1, 0.0, -0.1, 0.0))

INIT_CLR = np.array(((255, 255, 255), (220, 160, 110), (54, 125, 200), (110, 200, 125), (180, 64, 190)))
INIT_MASS = np.array((0.0, 1.0, 1.0, 1.0, 1.0))
INIT_RAD = np.array((2.0, 4.0, 4.0, 4.0, 4.0))
INIT_UNFIXED = np.array((1.0, 1.0, 1.0, 1.0, 1.0))
