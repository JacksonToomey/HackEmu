from rom import Rom


class Ram(Rom):
    KBD = 24576
    SCREEN = 16384

    def __init__(self, size, fromq, toq):
        self.fromq = fromq
        self.toq = toq
        super().__init__(size)

    def __setitem__(self, key, value):
        key = key % self._size
        self._registers[key].value = value
        if key >= self.SCREEN and key < self.KBD:
            self.toq.put((key - self.SCREEN, self._registers[key].value))

    def update_key_buffer(self):
        if not self.fromq.empty():
            val = self.fromq.get()
            self[self.KBD] = val


if __name__ == '__main__':
    r = Ram(32768)
    assert r[0] == 0

    r[0] = 1
    assert r[0] == 1

    r[32768] = 2
    assert r[0] == 2
