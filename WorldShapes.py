import pyglet
from pyglet import shapes
from constants import *


class WorldShapes:
    def __init__(self, world, grav_batch, out_batch, ui_batch):

        self.grid_rectangles = [[None for _ in range(NUM_ROWS)] for _ in range(NUM_COLS)]
        self.obj_points = [None for _ in range(world.num_objs)]
        self.grid_border = []
        self.select_pixel_rect = []

        self.init_shapes(world, grav_batch, out_batch, ui_batch)

    def init_shapes(self, world, grav_batch, out_batch, ui_batch):
        pixel_view = world.pixel_view

        for col in range(NUM_COLS):
            for row in range(NUM_ROWS):
                self.grid_rectangles[col][row] = shapes.Rectangle(col * GRID_LENGTH, row * GRID_LENGTH,
                                                                  GRID_LENGTH, GRID_LENGTH,
                                                                  color=(tuple(PIXEL_BACK_CLR)), batch=out_batch)

        for obj in range(world.num_objs):
            self.obj_points[obj] = shapes.Circle(SCREEN_WIDTH + world.obj_x[pixel_view, obj],
                                                 world.obj_y[pixel_view, obj], world.obj_rad[pixel_view, obj],
                                                 color=world.obj_clr[pixel_view, obj].astype(int), batch=grav_batch)

        # GRID LINES
        if GRID_LENGTH >= MIN_GRID_DISPLAY_LENGTH:
            for col in range(NUM_COLS):
                for row in range(NUM_ROWS):
                    self.extend_with_rectangle_border(self.grid_border, col * GRID_LENGTH, row * GRID_LENGTH,
                                                      GRID_LENGTH, GRID_LENGTH, 1, (64, 64, 64, 128), ui_batch)

        # SELECTED PIXEL GRID LINE HIGHLIGHT
        self.extend_with_rectangle_border(self.select_pixel_rect, 0, 0, GRID_LENGTH, GRID_LENGTH,
                                          1, (255, 255, 255, 128), ui_batch)

        # SELECTED OBJECT HIGHLIGHT
        self.extend_with_rectangle_border(self.select_pixel_rect, 0, 0, GRID_LENGTH, GRID_LENGTH,
                                          1, (255, 255, 255, 128), ui_batch)

        self.set_select_pixel_shape(pixel_view)

    @staticmethod
    def extend_with_rectangle_border(shape_list, x, y, width, height, border, clr, batch):
        shape_list.extend([shapes.Rectangle(x, y, width, border, color=clr, batch=batch)])
        shape_list.extend([shapes.Rectangle(x, y, border, height, color=clr, batch=batch)])
        shape_list.extend([shapes.Rectangle(x, y + height, width, -border, color=clr, batch=batch)])
        shape_list.extend([shapes.Rectangle(x + width, y, -border, height, color=clr, batch=batch)])

    @staticmethod
    def set_rectangle_border_pos(shape_list, index, x, y):
        dx = x - shape_list[index].x
        dy = y - shape_list[index].y

        shape_list[index].x += dx
        shape_list[index + 1].x += dx
        shape_list[index + 2].x += dx
        shape_list[index + 3].x += dx

        shape_list[index].y += dy
        shape_list[index + 1].y += dy
        shape_list[index + 2].y += dy
        shape_list[index + 3].y += dy

    def set_select_pixel_shape(self, pixel_view):
        px = pixel_view % NUM_COLS
        py = pixel_view // NUM_COLS
        self.set_rectangle_border_pos(self.select_pixel_rect, 0, px * GRID_LENGTH, py * GRID_LENGTH)