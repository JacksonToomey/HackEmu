from rom import Rom


class Ram(Rom):
    def __init__(self, size):
        super().__init__(size)

    def __setitem__(self, key, value):
        key = key % self._size
        self._registers[key].value = value


if __name__ == '__main__':
    r = Ram(32768)
    assert r[0] == 0

    r[0] = 1
    assert r[0] == 1

    r[32768] = 2
    assert r[0] == 2
