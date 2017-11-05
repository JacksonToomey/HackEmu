from register import Register


class Rom(object):
    def __init__(self, size, data=None):
        if data is None:
            data = []
        self._size = size
        self._registers = {}
        for x in range(size):
            value = 0
            if len(data) > x:
                value = data[x]
            self._registers[x] = Register(value)

    @property
    def size(self):
        return self._size

    def __getitem__(self, key):
        key = key % self._size
        return self._registers[key].value


if __name__ == '__main__':
    r = Rom(32768)

    assert r.size == 32768

    assert r[0] == 0

    try:
        r[0] = 2
        assert 1 == 2
    except Exception as ex:
        assert isinstance(ex, TypeError)

    r = Rom(32768, data=[0x000f])
    assert r[0] == 15
    assert r[1] == 0

    r = Rom(32768, data=[0x0001, 0x0000, 0xffff])
    assert r[0] == 1
    assert r[1] == 0
    assert r[2] == -1
    assert r[3] == 0
