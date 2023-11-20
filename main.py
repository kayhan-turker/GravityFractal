from World import *
import pyglet

# WINDOW AND BATCH CREATION

window = pyglet.window.Window(width=SCREEN_WIDTH * 2, height=SCREEN_HEIGHT)

out_batch = pyglet.graphics.Batch()
grav_batch = pyglet.graphics.Batch()
world = World(grav_batch, out_batch)


@window.event
def on_draw():
    window.clear()
    grav_batch.draw()
    out_batch.draw()


def update(dt):
    world.update()


pyglet.clock.schedule_interval(update, 1 / 60.0)
pyglet.app.run()
