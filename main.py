from World import *
import pyglet

# WINDOW AND BATCH CREATION

window = pyglet.window.Window(width=SCREEN_WIDTH * 2, height=SCREEN_HEIGHT)

out_batch = pyglet.graphics.Batch()
grav_batch = pyglet.graphics.Batch()
ui_batch = pyglet.graphics.Batch()

clear_mode = True
ui_grid = True

world = World(grav_batch, out_batch, ui_batch)
fps_display = pyglet.window.FPSDisplay(window=window)
fps_display.label.x = SCREEN_WIDTH * 2 - 105


@window.event
def on_draw():
    if clear_mode:
        window.clear()
    grav_batch.draw()
    out_batch.draw()
    if ui_grid:
        ui_batch.draw()
    if clear_mode:
        fps_display.draw()


def update(dt):
    world.update()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == 1 and 0 < x < 2 * SCREEN_WIDTH and 0 < y < SCREEN_HEIGHT:
        click_x = x // GRID_LENGTH % NUM_COLS
        click_y = y // GRID_LENGTH
        world.set_pixel_view(click_x + click_y * NUM_COLS)


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons == 1 and 0 < x < 2 * SCREEN_WIDTH and 0 < y < SCREEN_HEIGHT:
        click_x = x // GRID_LENGTH % NUM_COLS
        click_y = y // GRID_LENGTH
        world.set_pixel_view(click_x + click_y * NUM_COLS)


def check_move_pixel(symbol):
    if symbol == pyglet.window.key.LEFT:
        px = max(world.pixel_view % NUM_COLS - 1, 0)
        py = world.pixel_view // NUM_ROWS
        world.set_pixel_view(px + py * NUM_COLS)
    if symbol == pyglet.window.key.RIGHT:
        px = min(world.pixel_view % NUM_COLS + 1, NUM_COLS)
        py = world.pixel_view // NUM_ROWS
        world.set_pixel_view(px + py * NUM_COLS)
    if symbol == pyglet.window.key.DOWN:
        px = world.pixel_view % NUM_COLS
        py = max(world.pixel_view // NUM_ROWS - 1, 0)
        world.set_pixel_view(px + py * NUM_COLS)
    if symbol == pyglet.window.key.UP:
        px = world.pixel_view % NUM_COLS
        py = min(world.pixel_view // NUM_ROWS + 1, NUM_ROWS)
        world.set_pixel_view(px + py * NUM_COLS)


@window.event
def on_key_press(symbol, modifiers):
    global clear_mode, ui_grid
    check_move_pixel(symbol)

    if symbol == pyglet.window.key._1:
        ui_grid = not ui_grid
    if symbol == pyglet.window.key._2:
        window.clear()
        clear_mode = not clear_mode

pyglet.clock.schedule_interval(update, 1 / 60.0)
pyglet.app.run()
