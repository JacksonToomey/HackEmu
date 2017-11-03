import pyglet
import sys
from hack import Hack
from utility import int_to_16_bit


window = pyglet.window.Window()


def update(dt):
    cpu.execute()


@window.event
def on_draw():
    batch = pyglet.graphics.Batch()
    window.clear()
    screen_adr = 16384
    for x in range(8192):
        reg_addr = screen_adr + x
        bin_val = int_to_16_bit(cpu.ram[reg_addr])
        pixel_count = 0
        pixels = []
        row = x // 32
        col_offset = x % 32
        for i, b in enumerate(bin_val):
            if b == '1':
                pixels.extend([col_offset + i, row])
        if pixel_count:
            batch.add(pixel_count, pyglet.gl.GL_POINTS, None, ('v2i', pixels))
    batch.draw()


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print('Error: Rom file required')
        sys.exit(1)
    global cpu
    rom_file = args[0]
    with open(rom_file, 'r+') as rm:
        data = rm.read()
        data = data.split('\n')
        if '' in data:
            data = []
    cpu = Hack(data)
    pyglet.clock.schedule_interval(update, 0.01)
    pyglet.app.run()
