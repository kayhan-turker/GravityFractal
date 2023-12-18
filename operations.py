from constants import *


OBJ_SELECT_MIN_RADIUS = 32


def get_clicked_obj(mouse_x, mouse_y, world):
    current_pixel = world.pixel_view

    for i in range(world.num_objs):
        if world.obj_active[current_pixel, i]:
            dx = mouse_x - world.obj_x[current_pixel, i]
            dy = mouse_y - world.obj_y[current_pixel, i]
            dist = dx * dx + dy * dy
            rad = max(OBJ_SELECT_MIN_RADIUS, world.obj_rad[current_pixel, i])

            if dist < rad * rad:
                print(i)
                return i
    return None


def set_obj_pos(mouse_x, mouse_y, world):
    click_x = mouse_x // GRID_LENGTH % NUM_COLS
    click_y = mouse_y // GRID_LENGTH
    world.set_pixel_view(click_x + click_y * NUM_COLS)


def set_pixel_view(mouse_x, mouse_y, world):
    click_x = mouse_x // GRID_LENGTH % NUM_COLS
    click_y = mouse_y // GRID_LENGTH
    world.set_pixel_view(click_x + click_y * NUM_COLS)
