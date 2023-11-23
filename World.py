from pyglet import shapes
from init_params import *
from helper_functions import *
import numpy as np
import math


class World:
    def __init__(self, grav_batch, out_batch, ui_batch):
        self.obj_x = None
        self.obj_y = None
        self.obj_vx = None
        self.obj_vy = None
        self.obj_clr = None
        self.obj_mass = None
        self.obj_rad = None
        self.obj_active = None

        self.num_pixels = NUM_COLS * NUM_ROWS
        self.num_objs = None
        self.track_obj = 0

        self.init_objs()

        self.grid_rectangles = [[None for _ in range(NUM_ROWS)] for _ in range(NUM_COLS)]
        self.obj_points = [None for _ in range(self.num_objs)]
        self.grid_border = []
        self.select_pixel_rect = []

        self.combine_list = np.array([])
        self.zero_track_mass = INIT_MASS[self.track_obj] == 0

        self.timer = 0
        self.pixel_clr_sum = np.zeros((self.num_pixels, 3))
        self.pixel_last_collide = np.ones(self.num_pixels) * self.track_obj
        self.pixel_num_collide = np.zeros(self.num_pixels, dtype=int)
        self.pixel_view = 0

        self.init_shapes(grav_batch, out_batch, ui_batch)

    def init_shapes(self, grav_batch, out_batch, ui_batch):
        for col in range(NUM_COLS):
            for row in range(NUM_ROWS):
                self.grid_rectangles[col][row] = shapes.Rectangle(col * GRID_LENGTH, row * GRID_LENGTH,
                                                                  GRID_LENGTH, GRID_LENGTH,
                                                                  color=(0, 0, 0), batch=out_batch)

        for obj in range(self.num_objs):
            self.obj_points[obj] = shapes.Circle(SCREEN_WIDTH + self.obj_x[self.pixel_view, obj],
                                                 self.obj_y[self.pixel_view, obj], self.obj_rad[self.pixel_view, obj],
                                                 color=self.obj_clr[self.pixel_view, obj].astype(int), batch=grav_batch)

        if GRID_LENGTH > 7:
            for col in range(NUM_COLS):
                for row in range(NUM_ROWS):
                    extend_with_rectangle_border(self.grid_border, col * GRID_LENGTH, row * GRID_LENGTH,
                                                 GRID_LENGTH, GRID_LENGTH, 1, (64, 64, 64, 128), ui_batch)

        extend_with_rectangle_border(self.select_pixel_rect, 0, 0, GRID_LENGTH, GRID_LENGTH,
                                     1, (255, 255, 255, 128), ui_batch)
        self.set_select_pixel_shape()

    def init_objs(self):
        self.num_objs = len(INIT_MASS)

        self.obj_x = np.tile(INIT_X.copy()[:self.num_objs], (self.num_pixels, 1))
        self.obj_y = np.tile(INIT_Y.copy()[:self.num_objs], (self.num_pixels, 1))

        for p in range(self.num_pixels):
            px = p % NUM_COLS
            py = p // NUM_COLS
            self.obj_x[p, self.track_obj] = (px + 0.5) * GRID_LENGTH
            self.obj_y[p, self.track_obj] = (py + 0.5) * GRID_LENGTH

        self.obj_vx = np.tile(INIT_VX.copy()[:self.num_objs], (self.num_pixels, 1))
        self.obj_vy = np.tile(INIT_VY.copy()[:self.num_objs], (self.num_pixels, 1))

        self.obj_clr = np.tile(INIT_CLR.copy()[:self.num_objs], (self.num_pixels, 1, 1))
        self.obj_mass = np.tile(INIT_MASS.copy()[:self.num_objs], (self.num_pixels, 1))
        self.obj_rad = np.tile(INIT_RAD.copy()[:self.num_objs], (self.num_pixels, 1))

        self.obj_active = np.ones((self.num_pixels, self.num_objs))

    def update(self):
        self.simulate()
        self.process_combine_list()
        self.update_pixels()

    def simulate(self):
        num_objs = self.num_objs

        # get distance matrix
        dx = np.tile(np.expand_dims(self.obj_x.copy(), 2), (1, 1, num_objs))
        dy = np.tile(np.expand_dims(self.obj_y.copy(), 2), (1, 1, num_objs))
        dx = dx.transpose((0, 2, 1)) - dx
        dy = dy.transpose((0, 2, 1)) - dy
        dist_squared = dx * dx + dy * dy
        dist_squared = np.where(dist_squared == 0, 1.0, dist_squared)
        dist = np.sqrt(dist_squared)

        # get active
        active_array = np.expand_dims(self.obj_active.copy(), 2)
        active_array = active_array * active_array.transpose(0, 2, 1)

        # check if active objects collided
        sum_rad = np.expand_dims(self.obj_rad, 2)
        sum_rad = sum_rad + sum_rad.transpose(0, 2, 1)
        collided_objs = (dist < sum_rad) * active_array
        collided_objs[:, np.tril_indices(self.num_objs, k=0), np.tril_indices(self.num_objs, k=0)] = 0

        # convert collided to list to combine
        self.combine_list = collided_objs.copy()
        self.combine_list[:, np.tri(self.num_objs, k=0, dtype=bool)] = 0
        self.combine_list = np.column_stack(np.where(self.combine_list))

        # get gravity force (only if active toward objs not collided with)
        mag = active_array * (1 - collided_objs) / (dist_squared * dist) * GRAV_CONST * SIM_SPEED
        mag = mag * np.expand_dims(self.obj_mass, 1)

        # add to velocity
        self.obj_vx += np.sum(mag * dx, 2)
        self.obj_vy += np.sum(mag * dy, 2)

        for obj in range(num_objs):
            for other in range(obj + 1, num_objs):
                for p in range(self.num_pixels):
                    if collided_objs[p, obj, other]:

                        if obj == self.track_obj or other == self.track_obj:

                            hit_obj = obj if obj != self.track_obj else other

                            if hit_obj != self.pixel_last_collide[p] and self.pixel_num_collide[p] != NUM_COLLISION_DRAWS:

                                pixel_clr = np.array((0, 0, 0), dtype=np.float16) if hit_obj is None else self.obj_clr[
                                    p, hit_obj]
                                time_const = 1.0 / (self.timer * OUTPUT_CONTRAST / 255 + 1)
                                pixel_clr = pixel_clr * time_const
                                self.pixel_clr_sum[p] += pixel_clr * COLLISION_BRIGHTNESS[self.pixel_num_collide[p]]

                                px = p % NUM_COLS
                                py = p // NUM_COLS
                                self.grid_rectangles[px][py].color = (self.pixel_clr_sum[p]).astype(int)

                                self.pixel_last_collide[p] = hit_obj
                                self.pixel_num_collide[p] += 1

        self.obj_x += self.obj_vx * self.obj_active * SIM_SPEED
        self.obj_y += self.obj_vy * self.obj_active * SIM_SPEED
        self.check_wall_collision()

        self.timer += SIM_SPEED

    def check_wall_collision(self):
        x = self.obj_x
        y = self.obj_y
        if WALL_COLLISION:
            pass_x = np.where(x > SCREEN_WIDTH, x - SCREEN_WIDTH, np.where(x < 0, x, 0)) * self.obj_active
            pass_y = np.where(y > SCREEN_HEIGHT, y - SCREEN_HEIGHT, np.where(y < 0, y, 0)) * self.obj_active

            if np.any(pass_x != 0) or np.any(pass_y != 0):
                self.obj_x -= pass_x
                self.obj_y -= pass_y
                self.obj_vx *= np.where(pass_x == 0, 1, -1)
                self.obj_vy *= np.where(pass_y == 0, 1, -1)

    def process_combine_list(self):
        num_pairs = self.combine_list.shape[0]
        if num_pairs == 0:
            return

        for i in range(num_pairs):
            p, a, b = tuple(self.combine_list[i])
            if a == b:
                continue

            # combine (for all pixels if pixel doesnt change outcome)
            combine_for_all_pixels = self.zero_track_mass and a != self.track_obj and b != self.track_obj
            p_range = None if combine_for_all_pixels else p
            self.combine_obj_into(p_range, a, b)
            self.disable_obj(p_range, b)
            if p_range == self.pixel_view or p_range is None:
                self.update_obj_draw(a, False, True)
                self.update_obj_draw(b, True, False)

            # set new track object if it combined
            if a == self.track_obj or b == self.track_obj:
                self.track_obj = a
                self.zero_track_mass = self.zero_track_mass and self.obj_mass[p, self.track_obj] == 0

            # replace next pairs with new id if collided with something else
            for j in range(i + 1, num_pairs):
                p_next, a_next, b_next = tuple(self.combine_list[j])
                # check where ever combinations are being done
                if p_next == p or combine_for_all_pixels:
                    if a_next == b or b_next == b:
                        self.combine_list[j, 1:] = [a if x == b else a_next for x in self.combine_list[j][1:]]
                        #self.combine_list[j, 1:] = np.where(self.combine_list[j, 1:] == b, a, self.combine_list[j, 1:])

        self.combine_list = np.array([])

    def combine_obj_into(self, p, a, b):
        i, j = (p if p is not None else 0, p + 1 if p is not None else self.num_pixels)

        ma = self.obj_mass[i:j, a]
        mb = self.obj_mass[i:j, b]
        ma_abs = np.abs(ma)
        mb_abs = np.abs(mb)
        mt = ma + mb
        mt_abs = ma_abs + mb_abs
        ra = np.where(mt == 0, 0.5, ma_abs / mt_abs)
        rb = np.where(mt == 0, 0.5, mb_abs / mt_abs)

        self.obj_x[i:j, a] = self.obj_x[i:j, a] * ra + self.obj_x[i:j, b] * rb
        self.obj_y[i:j, a] = self.obj_y[i:j, a] * ra + self.obj_y[i:j, b] * rb
        self.obj_vx[i:j, a] = self.obj_vx[i:j, a] * ra + self.obj_vx[i:j, b] * rb
        self.obj_vy[i:j, a] = self.obj_vy[i:j, a] * ra + self.obj_vy[i:j, b] * rb

        self.obj_mass[i:j, a] = mt
        self.obj_rad[i:j, a] = self.obj_rad[i:j, a] * ra + self.obj_rad[i:j, b] * rb
        self.obj_clr[i:j, a] = (self.obj_clr[i:j, a] * ra[:, np.newaxis] +
                                self.obj_clr[i:j, b] * rb[:, np.newaxis])

    def disable_obj(self, p, obj):
        i, j = (p if p is not None else 0, p + 1 if p is not None else self.num_pixels)
        new_pos = self.obj_rad[i:j, obj]
        self.obj_x[i:j, obj] = -new_pos
        self.obj_y[i:j, obj] = -new_pos
        self.obj_active[i:j, obj] = 0

    def update_obj_draw(self, obj, update_pos=True, update_shape=True):
        pixel = self.pixel_view
        if update_pos:
            self.obj_points[obj].x = self.obj_x[pixel, obj] + SCREEN_WIDTH
            self.obj_points[obj].y = self.obj_y[pixel, obj]
        if update_shape:
            self.obj_points[obj].radius = self.obj_rad[pixel, obj]
            self.obj_points[obj].color = self.obj_clr[pixel, obj].astype(int)

    def update_pixels(self):
        for obj in range(self.num_objs):
            self.update_obj_draw(obj, True, False)

    def set_pixel_view(self, pixel):
        self.pixel_view = pixel
        for obj in range(self.num_objs):
            self.update_obj_draw(obj)
        self.set_select_pixel_shape()

    def set_select_pixel_shape(self):
        px = self.pixel_view % NUM_COLS
        py = self.pixel_view // NUM_COLS
        set_rectangle_border_pos(self.select_pixel_rect, 0, px * GRID_LENGTH, py * GRID_LENGTH)