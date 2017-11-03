from ram import Ram
from rom import Rom
from register import Register
from utility import match_bitmask


class Hack(object):
    A_INSTRUCTION = 4096
    LOAD_OP = -32768
    BITWISE_AND = 0
    CONSTANT_ZERO = 2688

    def __init__(self, data=None):
        self.ram = Ram(32768)
        self.rom = Rom(32768, data=data)
        self.register_a = Register()
        self.register_d = Register()
        self.program_counter = Register()

    def execute(self):
        if self.is_load_op:
            self.register_a.value = self.instruction
        else:
            comp = self.comp
            for d in self.destinations:
                d.value = comp
            self.program_counter.value = self.next_instruction

    @property
    def comp(self):
        if match_bitmask(self.instruction, self.CONSTANT_ZERO):
            return 0
        else:
            return self.register_d.value | self.memory_register_value

    @property
    def destinations(self):
        destinations = []
        return destinations

    @property
    def next_instruction(self):
        current = self.program_counter.value
        return current + 1

    @property
    def memory_register_value(self):
        is_a = match_bitmask(self.instruction, self.A_INSTRUCTION)
        if is_a:
            return self.register_a.value
        else:
            return self.ram[self.register_a.value]

    @memory_register_value.setter
    def memory_register_value(self, value):
        is_a = match_bitmask(self.instruction, self.A_INSTRUCTION)
        if is_a:
            self.register_a.value = value
        else:
            self.ram[self.register_a.value] = value

    @property
    def is_load_op(self):
        return not match_bitmask(self.instruction, self.LOAD_OP)

    @property
    def instruction(self):
        return self.rom[self.program_counter.value]


if __name__ == '__main__':
    h = Hack(['0000000000000001'])
    h.execute()
    assert h.register_a.value == 1

    h = Hack(['0000000000000111'])
    h.execute()
    assert h.register_a.value == 7

    h = Hack(['0111111111111111'])
    h.execute()
    assert h.register_a.value == 32767

    h = Hack(['1110000000000000'])
    h.execute()
    assert h.register_a.value == 0
    assert h.register_d.value == 0
    assert h.program_counter.value == 1
