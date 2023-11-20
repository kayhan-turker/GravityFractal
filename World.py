from pyglet import shapes
from constants import *
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

        self.num_objs = None

        self.start_x = 0
        self.start_y = 0

        self.init_objs()

        self.grid_rectangles = [[None for _ in range(NUM_ROWS)] for _ in range(NUM_COLS)]
        self.obj_points = [None for _ in range(self.num_objs)]

        self.combine_list = []

        self.timer = 0

        for col in range(NUM_COLS):
            for row in range(NUM_ROWS):
                self.grid_rectangles[col][row] = shapes.Rectangle(col * GRID_LENGTH, row * GRID_LENGTH,
                                                                  GRID_LENGTH, GRID_LENGTH,
                                                                  color=(0, 0, 0), batch=out_batch)

        for obj in range(self.num_objs):
            self.obj_points[obj] = shapes.Circle(SCREEN_WIDTH + self.obj_x[obj], self.obj_y[obj],
                                                 self.obj_rad[obj], color=self.obj_clr[obj], batch=grav_batch)

    def init_objs(self):

        self.obj_x = INIT_X.copy()
        self.obj_y = INIT_Y.copy()
        self.obj_x[TRACK_INDEX] = (self.start_x + 0.5) * GRID_LENGTH
        self.obj_y[TRACK_INDEX] = (self.start_y + 0.5) * GRID_LENGTH
        self.obj_vx = INIT_VX.copy()
        self.obj_vy = INIT_VY.copy()

        self.obj_clr = INIT_CLR.copy()
        self.obj_mass = INIT_MASS.copy()
        self.obj_rad = INIT_RAD.copy()

        self.num_objs = len(self.obj_x)

        self.obj_active = np.ones(self.num_objs)

    def end_round(self, hit_obj):

        self.combine_list.clear()

        pixel_clr = (0, 0, 0) if hit_obj is None else self.obj_clr[hit_obj]
        time_const = 1.0 / (PIXEL_CONTRAST * self.timer + 1)
        pixel_clr = [round(pixel_clr[i] * time_const) for i in range(3)]
        self.grid_rectangles[self.start_x][self.start_y].color = pixel_clr

        self.timer = 0
        self.start_x += 1
        if self.start_x >= NUM_COLS:
            self.start_x = 0
            self.start_y += 1
        if self.start_y >= NUM_ROWS:
            self.start_x = 0
            self.start_y = 0

        self.init_objs()
        for i in range(self.num_objs):
            self.obj_points[i].radius = self.obj_rad[i]
            self.obj_points[i].color = self.obj_clr[i]

    def update(self):
        self.simulate()
        self.combine()
        self.update_pixels()

    def simulate(self):
        for obj in range(self.num_objs):
            if self.obj_active[obj] == 0:
                continue

            for other in range(obj + 1, self.num_objs):
                if self.obj_active[other] == 0:
                    continue

                ma = self.obj_mass[obj]
                mb = self.obj_mass[other]
                dx = self.obj_x[other] - self.obj_x[obj]
                dy = self.obj_y[other] - self.obj_y[obj]
                dist_squared = dx * dx + dy * dy
                dist = math.sqrt(dist_squared)

                if dist > self.obj_rad[obj] + self.obj_rad[other]:
                    mag = GRAV_CONST / dist_squared / dist * SIM_SPEED
                    self.obj_vx[obj] += mb * dx * mag
                    self.obj_vy[obj] += mb * dy * mag
                    self.obj_vx[other] -= ma * dx * mag
                    self.obj_vy[other] -= ma * dy * mag
                else:
                    if obj == TRACK_INDEX or other == TRACK_INDEX:
                        self.end_round(obj if obj != TRACK_INDEX else other)
                        return
                    self.combine_list.append([min(obj, other), max(obj, other)])

        for obj in range(self.num_objs):
            if self.obj_active[obj] == 0:
                continue
            self.obj_x[obj] += self.obj_vx[obj] * SIM_SPEED
            self.obj_y[obj] += self.obj_vy[obj] * SIM_SPEED

        self.timer += SIM_SPEED
        if self.timer > TIME_LIMIT:
            self.end_round(None)

    def combine(self):
        len_list = len(self.combine_list)
        if len_list == 0:
            return

        for i in range(len_list):
            a = self.combine_list[i][0]
            b = self.combine_list[i][1]
            if a == b:
                continue

            ma = self.obj_mass[a]
            mb = self.obj_mass[b]
            if ma == 0 and mb == 0:
                ma = 1
                mb = 1
            mt = ma + mb

            ra = self.obj_rad[a]
            rb = self.obj_rad[b]

            self.obj_x[a] = self.obj_x[a] * ma / mt + self.obj_x[b] * mb / mt
            self.obj_y[a] = self.obj_y[a] * ma / mt + self.obj_y[b] * mb / mt
            self.obj_vx[a] = self.obj_vx[a] * ma / mt + self.obj_vx[b] * mb / mt
            self.obj_vy[a] = self.obj_vy[a] * ma / mt + self.obj_vy[b] * mb / mt

            self.obj_mass[a] = mt
            self.obj_rad[a] = (mt * mt / (ma * ma / ra / ra / ra + mb * mb / rb / rb / rb)) ** (1 / 3)
            self.obj_points[a].radius = self.obj_rad[a]
            self.obj_clr[a] = self.obj_clr[a] * ma / mt + self.obj_clr[b] * mb / mt
            self.obj_points[a].color = self.obj_clr[a]

            self.obj_active[b] = 0
            self.obj_points[b].x = -self.obj_rad[b]
            self.obj_points[b].y = -self.obj_rad[b]

            for j in range(i, len_list):
                if self.combine_list[j][0] == b:
                    self.combine_list[j][0] = a
                if self.combine_list[j][1] == b:
                    self.combine_list[j][0] = a

        self.combine_list.clear()

    def update_pixels(self):
        for obj in range(self.num_objs):
            if self.obj_active[obj] == 0:
                continue

            self.obj_points[obj].x = SCREEN_WIDTH + self.obj_x[obj]
            self.obj_points[obj].y = self.obj_y[obj]
