from pyglet import shapes
from init_params import *
import numpy as np


class World:
    def __init__(self, grav_batch, out_batch):

        self.obj_x = None
        self.obj_y = None
        self.obj_vx = None
        self.obj_vy = None
        self.obj_clr = None
        self.obj_mass = None
        self.obj_rad = None
        self.obj_unfixed = None

        self.num_pixels = NUM_COLS * NUM_ROWS
        self.num_objs = None
        self.pixel_complete = None

        self.init_objs()

        self.grid_rectangles = [[None for _ in range(NUM_ROWS)] for _ in range(NUM_COLS)]
        self.obj_points = [None for _ in range(self.num_objs)]

        self.combine_list = []

        self.timer = 0

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
        self.obj_unfixed = np.tile(INIT_UNFIXED.copy(), (self.num_pixels, 1))

        self.num_objs = len(INIT_MASS)
        self.pixel_complete = np.zeros(self.num_pixels)

    def update(self):
        self.simulate()
        self.combine()
        self.update_pixels()

    def simulate(self):
        for obj in range(self.num_objs):
            for other in range(obj + 1, self.num_objs):
                ma = self.obj_mass[:, obj]
                mb = self.obj_mass[:, other]
                dx = self.obj_x[:, other] - self.obj_x[:, obj]
                dy = self.obj_y[:, other] - self.obj_y[:, obj]
                dist_squared = dx * dx + dy * dy
                dist_squared = np.where(dist_squared == 0, 1.0, dist_squared)
                dist = np.sqrt(dist_squared)

                unfixed_a = self.obj_unfixed[:, obj]
                unfixed_b = self.obj_unfixed[:, other]

                mag = np.ones(self.num_pixels) / dist_squared / dist * GRAV_CONST * SIM_SPEED
                self.obj_vx[:, obj] += mb * dx * mag * unfixed_a
                self.obj_vy[:, obj] += mb * dy * mag * unfixed_a
                self.obj_vx[:, other] -= ma * dx * mag * unfixed_b
                self.obj_vy[:, other] -= ma * dy * mag * unfixed_b

                for p in range(self.num_pixels):
                    if dist[p] < self.obj_rad[p, obj] + self.obj_rad[p, other]:
                        if obj == TRACK_INDEX or other == TRACK_INDEX:
                            self.end_round(p, obj if obj != TRACK_INDEX else other)
                        self.combine_list.append([p, min(obj, other), max(obj, other)])

        self.obj_x += self.obj_vx * self.obj_unfixed * SIM_SPEED
        self.obj_y += self.obj_vy * self.obj_unfixed * SIM_SPEED

        self.timer += SIM_SPEED
        if self.timer > TIME_LIMIT:
            for p in range(self.num_pixels):
                self.end_round(p, None)

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

            ra = self.obj_rad[p, a]
            rb = self.obj_rad[p, b]
            ma = self.obj_mass[p, a]
            mb = self.obj_mass[p, b]
            if ma == 0 and mb == 0:
                ma = 1
                mb = 1
            mt = ma + mb

            self.obj_x[p, a] = self.obj_x[p, a] * ma / mt + self.obj_x[p, b] * mb / mt
            self.obj_y[p, a] = self.obj_y[p, a] * ma / mt + self.obj_y[p, b] * mb / mt
            self.obj_vx[p, a] = self.obj_vx[p, a] * ma / mt + self.obj_vx[p, b] * mb / mt
            self.obj_vy[p, a] = self.obj_vy[p, a] * ma / mt + self.obj_vy[p, b] * mb / mt

            self.obj_mass[p, a] = mt
            self.obj_rad[p, a] = (mt * mt / (ma * ma / ra / ra / ra + mb * mb / rb / rb / rb)) ** (1 / 3)
            self.obj_clr[p, a] = self.obj_clr[p, a] * ma / mt + self.obj_clr[p, b] * mb / mt

            self.obj_mass[p, b] = 0
            self.obj_unfixed[p, b] = 0

            if p == self.pixel_view:
                self.obj_points[b].x = -self.obj_rad[p, b]
                self.obj_points[b].y = -self.obj_rad[p, b]
                self.obj_points[a].radius = self.obj_rad[p, a]
                self.obj_points[a].color = self.obj_clr[p, a]

            for j in range(i + 1, len_list):
                combine_inst = self.combine_list[j]
                if combine_inst[0] == p:
                    if combine_inst[1] == b:
                        combine_inst[1] = a
                    if combine_inst[2] == b:
                        combine_inst[2] = a

        self.combine_list.clear()

    def end_round(self, p, hit_obj):
        if self.pixel_complete[p] == 1:
            return

        pixel_clr = (0, 0, 0) if hit_obj is None else self.obj_clr[p, hit_obj]
        time_const = 1.0 / (PIXEL_CONTRAST * self.timer + 1)
        pixel_clr = [round(pixel_clr[i] * time_const) for i in range(3)]

        px = p % NUM_COLS
        py = p // NUM_COLS
        self.grid_rectangles[px][py].color = pixel_clr

        # for i in range(self.num_objs):
        #    self.obj_points[i].radius = self.obj_rad[i]
        #    self.obj_points[i].color = self.obj_clr[i]

        self.pixel_complete[p] = 1

    def update_pixels(self):
        for obj in range(self.num_objs):
            self.obj_points[obj].x = SCREEN_WIDTH + self.obj_x[self.pixel_view, obj]
            self.obj_points[obj].y = self.obj_y[self.pixel_view, obj]
