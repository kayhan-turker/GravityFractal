from pyglet import shapes
from init_params import *
import numpy as np
import math


class World:
    def __init__(self, grav_batch, out_batch):

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
        self.pixel_active = None

        self.init_objs()

        self.grid_rectangles = [[None for _ in range(NUM_ROWS)] for _ in range(NUM_COLS)]
        self.obj_points = [None for _ in range(self.num_objs)]

        self.combine_list = []

        self.timer = 0
        self.pixel_clr_sum = np.zeros((self.num_pixels, 3))
        self.pixel_last_collide = np.ones(self.num_pixels) * TRACK_INDEX
        self.pixel_num_collide = np.zeros(self.num_pixels)
        self.pixel_view = 0

        for col in range(NUM_COLS):
            for row in range(NUM_ROWS):
                self.grid_rectangles[col][row] = shapes.Rectangle(col * GRID_LENGTH, row * GRID_LENGTH,
                                                                  GRID_LENGTH, GRID_LENGTH,
                                                                  color=(0, 0, 0), batch=out_batch)

        for obj in range(self.num_objs):
            self.obj_points[obj] = shapes.Circle(SCREEN_WIDTH + self.obj_x[self.pixel_view, obj],
                                                 self.obj_y[self.pixel_view, obj], self.obj_rad[self.pixel_view, obj],
                                                 color=self.obj_clr[self.pixel_view, obj], batch=grav_batch)

    def init_objs(self):

        self.obj_x = np.tile(INIT_X.copy(), (self.num_pixels, 1))
        self.obj_y = np.tile(INIT_Y.copy(), (self.num_pixels, 1))

        for p in range(self.num_pixels):
            px = p % NUM_COLS
            py = p // NUM_COLS
            self.obj_x[p, TRACK_INDEX] = (px + 0.5) * GRID_LENGTH
            self.obj_y[p, TRACK_INDEX] = (py + 0.5) * GRID_LENGTH

        self.obj_vx = np.tile(INIT_VX.copy(), (self.num_pixels, 1))
        self.obj_vy = np.tile(INIT_VY.copy(), (self.num_pixels, 1))

        self.obj_clr = np.tile(INIT_CLR.copy(), (self.num_pixels, 1, 1))
        self.obj_mass = np.tile(INIT_MASS.copy(), (self.num_pixels, 1))
        self.obj_rad = np.tile(INIT_RAD.copy(), (self.num_pixels, 1))

        self.num_objs = len(INIT_MASS)
        self.obj_active = np.ones((self.num_pixels, self.num_objs))
        self.pixel_active = np.ones((self.num_pixels, self.num_objs))

    def update(self):
        self.simulate()
        self.combine()
        self.update_pixels()

    def simulate(self):

        for p in range(self.num_pixels):
            if not self.pixel_active[p, 0]:
                continue

            for obj in range(self.num_objs):
                if not self.obj_active[p, obj]:
                    continue

                for other in range(obj + 1, self.num_objs):
                    if not self.obj_active[p, other]:
                        continue

                    ma = self.obj_mass[p, obj]
                    mb = self.obj_mass[p, other]
                    dx = self.obj_x[p, other] - self.obj_x[p, obj]
                    dy = self.obj_y[p, other] - self.obj_y[p, obj]
                    dist_squared = dx * dx + dy * dy
                    dist_squared = 1.0 if dist_squared == 0 else dist_squared
                    dist = math.sqrt(dist_squared)
                    sum_rad = self.obj_rad[p, obj] + self.obj_rad[p, other]

                    if dist > sum_rad * STOP_GRAV_FACTOR:
                        mag = 1.0 / dist_squared / dist * GRAV_CONST * SIM_SPEED
                        self.obj_vx[p, obj] += mb * dx * mag
                        self.obj_vy[p, obj] += mb * dy * mag
                        self.obj_vx[p, other] -= ma * dx * mag
                        self.obj_vy[p, other] -= ma * dy * mag

                    if dist < sum_rad:
                        if obj == TRACK_INDEX or other == TRACK_INDEX:
                            self.gather_pixel(p, obj if obj != TRACK_INDEX else other)
                            self.combine_list.append([p, TRACK_INDEX, obj if obj != TRACK_INDEX else other])
                        else:
                            self.combine_list.append([p, min(obj, other), max(obj, other)])

        self.obj_x += self.obj_vx * self.obj_active * self.pixel_active * SIM_SPEED
        self.obj_y += self.obj_vy * self.obj_active * self.pixel_active * SIM_SPEED

        self.timer += SIM_SPEED
        if self.timer > TIME_LIMIT:
            for p in range(self.num_pixels):
                self.gather_pixel(p, None)

    def combine(self):
        len_list = len(self.combine_list)
        if len_list == 0:
            return

        for i in range(len_list):
            p = self.combine_list[i][0]
            a = self.combine_list[i][1]
            b = self.combine_list[i][2]
            if a == b:
                continue

            if a != TRACK_INDEX and b != TRACK_INDEX and INIT_MASS[TRACK_INDEX] == 0.0:
                self.combine_objs_all_pixels(a, b)

                for j in range(i + 1, len_list):
                    combine_inst = self.combine_list[j]
                    if combine_inst[1] == b:
                        combine_inst[1] = a
                    if combine_inst[2] == b:
                        combine_inst[2] = a
            else:
                self.combine_objs_single_pixel(p, a, b)

                for j in range(i + 1, len_list):
                    combine_inst = self.combine_list[j]
                    if combine_inst[0] == p:
                        if combine_inst[1] == b:
                            combine_inst[1] = a
                        if combine_inst[2] == b:
                            combine_inst[2] = a

        self.combine_list.clear()

    def combine_objs_all_pixels(self, a, b):
        ma = self.obj_mass[:, a]
        mb = self.obj_mass[:, b]
        mt = ma + mb
        ma = np.where(mt == 0, 1.0, ma)
        mb = np.where(mt == 0, 1.0, mb)
        ma = ma / mt
        mb = mb / mt

        self.obj_x[:, a] = self.obj_x[:, a] * ma + self.obj_x[:, b] * mb
        self.obj_y[:, a] = self.obj_y[:, a] * ma + self.obj_y[:, b] * mb
        self.obj_vx[:, a] = self.obj_vx[:, a] * ma + self.obj_vx[:, b] * mb
        self.obj_vy[:, a] = self.obj_vy[:, a] * ma + self.obj_vy[:, b] * mb

        self.obj_mass[:, a] = mt
        self.obj_rad[:, a] = self.obj_rad[:, a] * ma + self.obj_rad[:, b] * mb
        ma_clr = np.tile(np.expand_dims(ma, 1), (1, 3))
        mb_clr = np.tile(np.expand_dims(mb, 1), (1, 3))
        self.obj_clr[:, a] = self.obj_clr[:, a] * ma_clr + self.obj_clr[:, b] * mb_clr

        self.obj_x[:, b] = -self.obj_rad[:, b]
        self.obj_y[:, b] = -self.obj_rad[:, b]
        self.obj_vx[:, b] = 0
        self.obj_vy[:, b] = 0
        self.obj_mass[:, b] = 0
        self.obj_active[:, b] = 0

        p = self.pixel_view
        self.obj_points[a].radius = self.obj_rad[p, a]
        self.obj_points[a].color = self.obj_clr[p, a]
        self.obj_points[b].x = self.obj_x[p, b]
        self.obj_points[b].y = self.obj_y[p, b]

    def combine_objs_single_pixel(self, p, a, b):
        ma = self.obj_mass[p, a]
        mb = self.obj_mass[p, b]
        if ma == 0 and mb == 0:
            ma = 1
            mb = 1
        mt = ma + mb
        ma = ma / mt
        mb = mb / mt

        self.obj_x[p, a] = self.obj_x[p, a] * ma + self.obj_x[p, b] * mb
        self.obj_y[p, a] = self.obj_y[p, a] * ma + self.obj_y[p, b] * mb
        self.obj_vx[p, a] = self.obj_vx[p, a] * ma + self.obj_vx[p, b] * mb
        self.obj_vy[p, a] = self.obj_vy[p, a] * ma + self.obj_vy[p, b] * mb

        self.obj_mass[p, a] = mt
        self.obj_rad[p, a] = self.obj_rad[p, a] * ma + self.obj_rad[p, b] * mb
        self.obj_clr[p, a] = self.obj_clr[p, a] * ma + self.obj_clr[p, b] * mb

        self.obj_x[p, b] = -self.obj_rad[p, b]
        self.obj_y[p, b] = -self.obj_rad[p, b]
        self.obj_vx[p, b] = 0
        self.obj_vy[p, b] = 0
        self.obj_mass[p, b] = 0
        self.obj_active[p, b] = 0

        if p == self.pixel_view:
            self.obj_points[a].radius = self.obj_rad[p, a]
            self.obj_points[a].color = self.obj_clr[p, a]
            self.obj_points[b].x = self.obj_x[p, b]
            self.obj_points[b].y = self.obj_y[p, b]

    def gather_pixel(self, p, hit_obj):
        if self.pixel_active[p, 0] == 0:
            return
        if COLOR_MODE == 1 and hit_obj == self.pixel_last_collide[p]:
            return

        px = p % NUM_COLS
        py = p // NUM_COLS

        pixel_clr = np.array((0, 0, 0), dtype=np.float16) if hit_obj is None else self.obj_clr[p, hit_obj]

        if COLOR_MODE == 0:

            time_const = 1.0 / (self.timer * PIXEL_CONTRAST / 255 + 1)
            pixel_clr = pixel_clr * time_const
            self.grid_rectangles[px][py].color = pixel_clr.astype(int)

            self.pixel_active[p, :] = 0

        elif COLOR_MODE == 1:
            self.pixel_last_collide[p] = hit_obj
            self.pixel_num_collide[p] += 1
            num_collide = self.pixel_num_collide[p]

            time_const = 1.0 / (self.timer * PIXEL_CONTRAST / 255 + 1)
            pixel_clr = pixel_clr * time_const
            # the 6 / pi^2 makes sure this sum converges to 1
            self.pixel_clr_sum[p] += pixel_clr * 6 / (num_collide * num_collide * PI * PI)
            self.grid_rectangles[px][py].color = (self.pixel_clr_sum[p]).astype(int)


    def update_pixels(self):
        for obj in range(self.num_objs):
            self.obj_points[obj].x = SCREEN_WIDTH + self.obj_x[self.pixel_view, obj]
            self.obj_points[obj].y = self.obj_y[self.pixel_view, obj]
