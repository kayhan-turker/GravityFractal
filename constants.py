
# 0 = opaque, time dependent brightness
# 1 = transparent, constant brightness (simulation does not end at collision)
COLOR_MODE = 1

# below this radius factor, no longer gather collision data
COLOR_MODE_1_BRIGHTNESS_FACTOR = 0.1

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRID_LENGTH = 4
NUM_COLS = SCREEN_WIDTH // GRID_LENGTH
NUM_ROWS = SCREEN_HEIGHT // GRID_LENGTH

GRAV_CONST = 1
SIM_SPEED = 4

# if distance is < sum radii * factor, stop gravitating
STOP_GRAV_FACTOR = 1

TRACK_INDEX = 0
TIME_LIMIT = 1000000000
PIXEL_CONTRAST = 0.25

PI = 3.1416