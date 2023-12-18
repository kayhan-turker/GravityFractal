import colorsys
import datetime
import os
from PIL import Image
from init_params import *
from WorldShapes import *


class World:
    def __init__(self, grav_batch, out_batch, ui_batch):
        self.obj_x = None
        self.obj_y = None
        self.obj_vx = None
        self.obj_vy = None
        self.obj_clr = None
        self.obj_mass = None
        self.obj_rad = None
        self.obj_free = None
        self.obj_active = None

        self.num_pixels = NUM_COLS * NUM_ROWS
        self.num_objs = None
        self.tracker_index = 0
        self.total_mass = 0

        self.init_objs()

        self.zero_track_mass = INIT_MASS[self.tracker_index] == 0

        self.timer = int(0)
        self.pixel_view = (NUM_ROWS * NUM_COLS - 1) // 2

        self.combine_list = np.array([])
        self.update_pixel_list = np.array([])

        self.tracker_collisions = np.array([])
        self.current_pixel_colors = np.ones((self.num_pixels, 3)) * PIXEL_BACK_CLR[None, :]
        self.remaining_hits = np.full(self.num_pixels, MAX_PIXEL_HITS)
        self.dx_matrix = np.array([])
        self.dy_matrix = np.array([])

        self.world_shapes = WorldShapes(self, grav_batch, out_batch, ui_batch)

        self.start_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        out_path = IMG_SAVE_PATH + self.start_time
        if not os.path.exists(out_path):
            os.makedirs(out_path)

        self.preview_mode = True
        self.clear_mode = True
        self.ui_grid = False

        self.selected_object = None

    def init_objs(self):
        self.num_objs = len(INIT_MASS)

        self.obj_x = np.tile(INIT_X.copy()[:self.num_objs], (self.num_pixels, 1))
        self.obj_y = np.tile(INIT_Y.copy()[:self.num_objs], (self.num_pixels, 1))

        for p in range(self.num_pixels):
            px = p % NUM_COLS
            py = p // NUM_COLS
            self.obj_x[p, self.tracker_index] = (px + 0.5) * GRID_LENGTH
            self.obj_y[p, self.tracker_index] = (py + 0.5) * GRID_LENGTH

        self.obj_vx = np.tile(INIT_VX.copy()[:self.num_objs], (self.num_pixels, 1))
        self.obj_vy = np.tile(INIT_VY.copy()[:self.num_objs], (self.num_pixels, 1))

        self.obj_clr = np.tile(INIT_CLR.copy()[:self.num_objs], (self.num_pixels, 1, 1))
        self.obj_rad = np.tile(INIT_RAD.copy()[:self.num_objs], (self.num_pixels, 1))
        self.obj_mass = np.tile(INIT_MASS.copy()[:self.num_objs], (self.num_pixels, 1))
        self.total_mass = np.sum(np.abs(self.obj_mass[0]))

        self.obj_free = np.tile(INIT_FREE.copy()[:self.num_objs], (self.num_pixels, 1))

        self.obj_active = np.full((self.num_pixels, self.num_objs), True, dtype=bool)

    def update(self):
        self.simulate()
        self.draw_update()                      # todo was it okay to move this before combine list???
        self.process_combine_list()
        self.timelapse_update()
        self.timer += SIM_SPEED

    def simulate(self):
        dist, dist_squared = self.get_distance_matrices()
        active_matrix = self.get_active_matrix()
        collided_objs = self.get_collided_object_matrix(dist, active_matrix)

        self.populate_combine_list(collided_objs)
        self.gravitate(active_matrix, collided_objs, dist, dist_squared)
        self.move_objects()

    def get_distance_matrices(self):
        self.dx_matrix = self.obj_x[:, None, :] - self.obj_x[:, :, None]
        self.dy_matrix = self.obj_y[:, None, :] - self.obj_y[:, :, None]
        dist_squared = self.dx_matrix * self.dx_matrix + self.dy_matrix * self.dy_matrix
        dist_squared = np.where(dist_squared == 0, 1.0, dist_squared)
        return np.sqrt(dist_squared), dist_squared

    def get_active_matrix(self):
        return self.obj_active[:, None, :] & self.obj_active[:, :, None]

    def get_collided_object_matrix(self, dist, active_matrix):
        sum_rad = self.obj_rad[:, :, None] + self.obj_rad[:, None, :]
        collided_objs = (dist < sum_rad) & active_matrix

        # remove diagonal (self collision doesn't count)
        collided_objs[:, np.tril_indices(self.num_objs, k=0), np.tril_indices(self.num_objs, k=0)] = False
        self.tracker_collisions = collided_objs[:, self.tracker_index]
        return collided_objs

    def populate_combine_list(self, collided_objs):
        self.combine_list = collided_objs.copy()

        # remove lower left triangle of matrix, to not repeat entries
        self.combine_list[:, np.tri(self.num_objs, k=0, dtype=bool)] = 0
        self.combine_list = np.argwhere(self.combine_list)

    def gravitate(self, active_matrix, collided_objs, dist, dist_squared):
        # get gravity force (only if active toward objs not collided with)
        mag = self.obj_free[:, :, None] * active_matrix * (GRAV_MATRIX if GRAV_MATRIX_MODE else GRAV_CONST)
        mag *= (1 - collided_objs) / (dist_squared * dist)
        mag = mag * np.expand_dims(self.obj_mass, 1)

        # add to velocity
        self.obj_vx += np.sum(mag * self.dx_matrix, 2)
        self.obj_vy += np.sum(mag * self.dy_matrix, 2)

    def process_update_pixel_list(self):
        self.update_pixel_list = np.argwhere(np.any(self.tracker_collisions * self.remaining_hits[:, None], 1)).flatten()
        if self.update_pixel_list.shape[0] == 0:
            return

        # get total new color from hit objects (for loop is more efficient)
        for p in self.update_pixel_list:

            if HUE_MODE == 0:
                clr_hue = self.obj_clr[p]
            else:
                hue_angle = np.arctan2(self.dx_matrix[p, self.tracker_index], self.dy_matrix[p, self.tracker_index])
                hue_angle = 0.75 - (hue_angle / PI / 2)
                hue_angle -= np.floor(hue_angle)
                hsv = np.column_stack((hue_angle, np.ones_like(hue_angle), np.ones_like(hue_angle)))
                clr_hue = np.array([colorsys.hsv_to_rgb(*values) for values in hsv]) * 255

            if VALUE_MODE == 0:
                clr_value_factor = 1 / (self.timer * PIXEL_TIME_CONTRAST / 255 + 1)
            else:
                vx = self.obj_vx[p, self.tracker_index]
                vy = self.obj_vy[p, self.tracker_index]
                vel = vx * vx + vy * vy
                clr_value_factor = vel * PIXEL_TIME_CONTRAST

            hit_clr = self.tracker_collisions[p, :, None] * (clr_hue - PIXEL_BACK_CLR)
            if MASS_WEIGHTED_TRANSPARENCY:
                hit_clr *= self.obj_mass[p, :, None] / self.total_mass
            hit_clr = np.sum(hit_clr, 0)

            hit_clr *= START_PIXEL_TRANSPARENCY * clr_value_factor
            hit_clr *= PIXEL_HIT_TRANSPARENCY[MAX_PIXEL_HITS - self.remaining_hits[p]]

            # account for background color
            current_clr = self.current_pixel_colors[p]
            new_clr = current_clr + np.where(hit_clr >= 0,
                                             hit_clr * (255 - current_clr) / (255 - PIXEL_BACK_CLR),
                                             hit_clr * current_clr / PIXEL_BACK_CLR)

            # update pixel colors
            px = p % NUM_COLS
            py = p // NUM_COLS
            self.current_pixel_colors[p] = new_clr
            self.world_shapes.grid_rectangles[px][py].color = tuple(np.clip(new_clr.astype(int), 0, 255))
            self.remaining_hits[p] -= 1

    def move_objects(self):
        self.obj_x += self.obj_vx * self.obj_active * SIM_SPEED
        self.obj_y += self.obj_vy * self.obj_active * SIM_SPEED
        self.check_wall_collision()

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
            p, a, b = self.combine_list[i]
            if a == b:
                continue

            # combine (for all pixels if pixel doesnt change outcome)
            combine_for_all_pixels = self.zero_track_mass and a != self.tracker_index and b != self.tracker_index
            p_range = None if combine_for_all_pixels else p
            self.combine_obj_into(p_range, a, b)
            self.disable_obj(p_range, b)
            if p_range == self.pixel_view or p_range is None:
                self.update_obj_draw(a, False, True)
                self.update_obj_draw(b, True, False)

            # set new track object if it combined
            if a == self.tracker_index or b == self.tracker_index:
                self.tracker_index = a
                self.zero_track_mass = self.zero_track_mass and self.obj_mass[p, self.tracker_index] == 0

            # update next values in the list with new indices
            check_list = self.combine_list[i + 1:]
            b_values = check_list[:, 1:] == b
            p_values = b_values if combine_for_all_pixels else (check_list[:, 0] == p)[:, None]
            check_list[:, 1:][p_values & b_values] = a

        self.combine_list = np.array([])

    def combine_obj_into(self, p, a, b):
        i, j = (p if p is not None else 0, p + 1 if p is not None else self.num_pixels)

        ma = self.obj_mass[i:j, a]
        mb = self.obj_mass[i:j, b]
        ma_abs = np.abs(ma)
        mb_abs = np.abs(mb)
        mt_abs = ma_abs + mb_abs
        ra_abs = np.where(mt_abs == 0, 0.5, ma_abs / mt_abs)
        rb_abs = np.where(mt_abs == 0, 0.5, mb_abs / mt_abs)

        self.obj_x[i:j, a] = self.obj_x[i:j, a] * ra_abs + self.obj_x[i:j, b] * rb_abs
        self.obj_y[i:j, a] = self.obj_y[i:j, a] * ra_abs + self.obj_y[i:j, b] * rb_abs
        self.obj_vx[i:j, a] = self.obj_vx[i:j, a] * ra_abs + self.obj_vx[i:j, b] * rb_abs
        self.obj_vy[i:j, a] = self.obj_vy[i:j, a] * ra_abs + self.obj_vy[i:j, b] * rb_abs

        self.obj_mass[i:j, a] = ma + mb
        self.obj_clr[i:j, a] = (self.obj_clr[i:j, a] * ra_abs[:, None] +
                                self.obj_clr[i:j, b] * rb_abs[:, None])

        if RADIUS_ADDITION_MODE == 0:
            self.obj_rad[i:j, a] = (self.obj_rad[i:j, a] * ra_abs[:, None] + self.obj_rad[i:j, b] * rb_abs[:, None])
        elif RADIUS_ADDITION_MODE == 1:
            self.obj_rad[i:j, a] = self.obj_rad[i:j, a] + self.obj_rad[i:j, b]
        elif RADIUS_ADDITION_MODE == 2:
            ra = self.obj_rad[i:j, a]
            rb = self.obj_rad[i:j, b]
            self.obj_rad[i:j, a] = np.cbrt(ra * ra * ra + rb * rb * rb)

        self.obj_free[i:j, a] = 1

    def disable_obj(self, p, obj):
        i, j = (p if p is not None else 0, p + 1 if p is not None else self.num_pixels)
        new_pos = self.obj_rad[i:j, obj]
        self.obj_x[i:j, obj] = -new_pos
        self.obj_y[i:j, obj] = -new_pos
        self.obj_active[i:j, obj] = 0

    def draw_update(self):
        # update pixel colors
        self.process_update_pixel_list()
        # update object positions
        for obj in range(self.num_objs):
            self.update_obj_draw(obj, True, False)

    def update_obj_draw(self, obj, update_pos=True, update_shape=True):
        pixel = self.pixel_view
        if update_pos:
            self.world_shapes.obj_points[obj].x = self.obj_x[pixel, obj] + SCREEN_WIDTH
            self.world_shapes.obj_points[obj].y = self.obj_y[pixel, obj]
        if update_shape:
            self.world_shapes.obj_points[obj].radius = self.obj_rad[pixel, obj]
            self.world_shapes.obj_points[obj].color = self.obj_clr[pixel, obj].astype(int)

    def set_pixel_view(self, pixel):
        self.pixel_view = pixel
        for obj in range(self.num_objs):
            self.update_obj_draw(obj)
        self.set_select_pixel_shape()

    def set_select_pixel_shape(self):
        px = self.pixel_view % NUM_COLS
        py = self.pixel_view // NUM_COLS
        self.world_shapes.set_rectangle_border_pos(self.world_shapes.select_pixel_rect, 0,
                                                   px * GRID_LENGTH, py * GRID_LENGTH)

    def timelapse_update(self):
        frame = round(self.timer / SIM_SPEED, 4)
        if TIMELAPSE_ENABLED and frame != 0 and frame % TIMELAPSE_FRAMES == 0:
            color_buffer = pyglet.image.get_buffer_manager().get_color_buffer()
            color_buffer = color_buffer.get_region(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
            image_data = color_buffer.get_image_data()
            buffer = image_data.get_data("RGBA", image_data.pitch)
            image_array = np.asarray(buffer).reshape((image_data.height, image_data.width, 4))
            image_array = np.flipud(image_array)

            image = Image.fromarray(image_array)
            path = IMG_SAVE_PATH + self.start_time + "/" + f"{frame:08.0f}.png"
            image.save(path)
