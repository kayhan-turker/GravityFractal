import pyglet.window.key
from World import *
from operations import *

# Set up Pyglet to use the Pillow image encoder
pyglet.options['image_codecs'] = ['pil']
# WINDOW AND BATCH CREATION

window = pyglet.window.Window(width=SCREEN_WIDTH * 2, height=SCREEN_HEIGHT)

out_batch = pyglet.graphics.Batch()
grav_batch = pyglet.graphics.Batch()
ui_batch = pyglet.graphics.Batch()


world = World(grav_batch, out_batch, ui_batch)
fps_display = pyglet.window.FPSDisplay(window=window)
fps_display.label.x = SCREEN_WIDTH * 2 - 105


@window.event
def on_draw():
    if world.clear_mode:
        window.clear()
    grav_batch.draw()
    out_batch.draw()
    if world.ui_grid:
        ui_batch.draw()
    if world.clear_mode:
        fps_display.draw()


def update(dt):
    world.update()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == 1 and 0 < x < 2 * SCREEN_WIDTH and 0 < y < SCREEN_HEIGHT:
        clicked_obj = get_clicked_obj(x, y, world)
        world.selected_object = clicked_obj
        if clicked_obj is None:
            set_pixel_view(x, y, world)


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons == 1 and 0 < x < 2 * SCREEN_WIDTH and 0 < y < SCREEN_HEIGHT:
        set_pixel_view(x, y, world)


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
    check_move_pixel(symbol)

    if symbol == pyglet.window.key.SPACE:
        PREVIEW_MODE = False

    if symbol == pyglet.window.key._1:
        world.ui_grid = not world.ui_grid
    if symbol == pyglet.window.key._2:
        window.clear()
        world.clear_mode = not world.clear_mode

pyglet.clock.schedule_interval(update, 1 / 60.0)
pyglet.app.run()
