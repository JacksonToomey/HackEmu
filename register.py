import struct
from utility import bound_value


class Register(object):
    WORD_STRUCT = struct.Struct('>h')

    def __init__(self, value=0):
        self._val = None
        self.value = value

    @property
    def value(self):
        val, = self.WORD_STRUCT.unpack(self._val)
        return val

    @value.setter
    def value(self, value):
        value = bound_value(value)
        self._val = self.WORD_STRUCT.pack(value)

    def __repr__(self):
        return str(self._val.hex())


if __name__ == '__main__':
    r = Register()
    assert r.value == 0
    assert str(r) == '0000'

    r.value = 2
    assert r.value == 2
    assert str(r) == '0002'

    r.value = -2
    assert r.value == -2
    assert str(r) == 'fffe'

    r.value = -1
    assert r.value == -1
    assert str(r) == 'ffff'

    r.value = 32767
    assert r.value == 32767
    assert str(r) == '7fff'

    r.value = -32768
    assert r.value == -32768
    assert str(r) == '8000'

    r.value = 32768
    assert r.value == -32768

    r.value = 32769
    assert r.value == -32767

    r.value = 65536
    assert r.value == 0

