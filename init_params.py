from constants import *

SX = SCREEN_WIDTH
SY = SCREEN_HEIGHT

INIT_X = np.array((0.0, 1 / 2, 1 / 4, 1 / 2, 3 / 4)) * SX
INIT_Y = np.array((0.0, 1 / 4, 1 / 2, 3 / 4, 1 / 2)) * SY

INIT_VX = np.array((0., 0., -0., 0., -0.)) * 0
INIT_VY = np.array((0., -0., 0., -0., 0.)) * 0

CLR_WHITE = (1.0, 1.0, 1.0)
CLR_BLACK = (0.0, 0.0, 0.0)
CLR_GREY = (0.5, 0.5, 0.5)
CLR_CUST_1 = (1.0, 0.1, 0.4)
CLR_CUST_2 = (1.0, 0.9, 0.4)
CLR_CUST_3 = (0.0, 1.0, 0.6)
CLR_CUST_4 = (0.2, 0.4, 1.0)
CLR_CUST_5 = (0.7, 0.2, 1.0)

INIT_CLR = np.array((CLR_WHITE, CLR_CUST_1, CLR_CUST_2, CLR_CUST_3, CLR_CUST_4), dtype=np.float16) * 255
INIT_MASS = np.array((1.0, 1.0, 1.0, 1.0, 1.0))
INIT_RAD = np.array((2.0, 2.0, 2.0, 2.0, 2.0))