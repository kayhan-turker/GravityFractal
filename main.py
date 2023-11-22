from World import *
import pyglet

# WINDOW AND BATCH CREATION

window = pyglet.window.Window(width=SCREEN_WIDTH * 2, height=SCREEN_HEIGHT)

out_batch = pyglet.graphics.Batch()
grav_batch = pyglet.graphics.Batch()
world = World(grav_batch, out_batch)
fps_display = pyglet.window.FPSDisplay(window=window)
fps_display.label.x = SCREEN_WIDTH * 2 - 90


@window.event
def on_draw():
    window.clear()
    grav_batch.draw()
    out_batch.draw()
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
        world.pixel_view = click_x + click_y * NUM_COLS


pyglet.clock.schedule_interval(update, 1 / 60.0)
pyglet.app.run()
