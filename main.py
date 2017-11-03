# import pyglet
# import random


# window = pyglet.window.Window()

# def update(dt):
#     print(dt)

# @window.event
# def on_draw():
#     batch = pyglet.graphics.Batch()
#     window.clear()
#     x1 = random.randint(10, 20)
#     x2 = random.randint(30, 40)
#     x3 = random.randint(100, 110)
#     x4 = random.randint(120, 150)
#     for x in range(8000):
#         batch.add(2, pyglet.gl.GL_POINTS, None, ('v2i', (x1, x2, x3, x4)))
#     batch.draw()

# pyglet.clock.schedule_interval(update, 0.01)
# pyglet.app.run()

if __name__ == '__main__':
    pass
