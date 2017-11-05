import pyglet
import sys
import time
import multiprocessing
from hack import Hack
from utility import int_to_16_bit


window = pyglet.window.Window(512, 256)


def worker(cpu):
    while True:
        cpu.execute()


def update(dt):
    while not from_cpu.empty():
        i, val = from_cpu.get()
        ram_list[i] = val


@window.event
def on_key_press(symbol, modifiers):
    to_cpu.put(-1)


@window.event
def on_key_release(symbol, modifiers):
    to_cpu.put(0)


@window.event
def on_draw():
    batch = pyglet.graphics.Batch()
    window.clear()
    for x, v in enumerate(ram_list):
        bin_val = int_to_16_bit(v)
        pixel_count = 0
        pixels = []
        row = x // 32
        row = 255 - row
        col_offset = (x % 32) * 16
        for i, b in enumerate(bin_val):
            if b == '1':
                pixels.extend([col_offset + i, row])
                pixel_count += 1
        if pixel_count:
            batch.add(
                pixel_count,
                pyglet.gl.GL_POINTS,
                None,
                ('v2i', pixels),
            )
    batch.draw()


@window.event
def on_close():
    cpu_worker.terminate()
    from_cpu.close()
    to_cpu.close()


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print('Error: Rom file required')
        sys.exit(1)
    global cpu_worker, from_cpu, to_cpu, ram_list
    ram_list = [0] * 8192
    rom_file = args[0]
    with open(rom_file, 'r+') as rm:
        data = rm.read()
        data = data.split('\n')
        if '' in data:
            data = []
    from_cpu = multiprocessing.Queue()
    to_cpu = multiprocessing.Queue()
    cpu = Hack(data, fromq=to_cpu, toq=from_cpu)
    cpu_worker = multiprocessing.Process(
        target=worker,
        args=(cpu,)
    )
    cpu_worker.start()
    pyglet.clock.schedule_interval(update, 0.01)
    pyglet.app.run()
