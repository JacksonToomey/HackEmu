from ram import Ram
from rom import Rom
from register import Register
from utility import match_bitmask


class Hack(object):
    A_INSTRUCTION = 4096
    LOAD_OP = -32768

    DEST_A = 32
    DEST_D = 16
    DEST_M = 8

    JGT = 1
    JEQ = 2
    JGE = 3
    JLT = 4
    JNE = 5
    JLE = 6
    JMP = 7

    D_BITWISE_AND_MEM = 0
    D_BITWISE_OR_MEM = 1344
    CONSTANT_ZERO = 2688
    CONSTANT_ONE = 3968
    CONSTANT_NEG_ONE = 3712
    D_REG = 768
    MEM_REG = 3072
    NOT_D = 832
    NOT_MEM = 3136
    NEG_D = 960
    NEG_MEM = 3264
    INCR_D = 1984
    INCR_MEM = 3520
    DEC_D = 896
    DEC_MEM = 3200
    D_PLUS_MEM = 128
    D_MINUS_MEM = 1216
    MEM_MINUS_D = 448

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
            self.load_destinations(comp)
            self.program_counter.value = self.get_next_instruction(comp)

    @property
    def comp(self):
        if match_bitmask(self.instruction, self.CONSTANT_ZERO):
            return 0
        elif match_bitmask(self.instruction, self.CONSTANT_ONE):
            return 1
        elif match_bitmask(self.instruction, self.CONSTANT_NEG_ONE):
            return -1
        elif match_bitmask(self.instruction, self.D_REG):
            return self.register_d.value
        elif match_bitmask(self.instruction, self.MEM_REG):
            return self.memory_register_value
        elif match_bitmask(self.instruction, self.NOT_D):
            return ~self.register_d.value
        elif match_bitmask(self.instruction, self.NOT_MEM):
            return ~self.memory_register_value
        elif match_bitmask(self.instruction, self.NEG_D):
            return -1 * self.register_d.value
        elif match_bitmask(self.instruction, self.NEG_MEM):
            return -1 * self.memory_register_value
        elif match_bitmask(self.instruction, self.INCR_D):
            return self.register_d.value + 1
        elif match_bitmask(self.instruction, self.INCR_MEM):
            return self.memory_register_value + 1
        elif match_bitmask(self.instruction, self.DEC_D):
            return self.register_d.value - 1
        elif match_bitmask(self.instruction, self.DEC_MEM):
            return self.memory_register_value - 1
        elif match_bitmask(self.instruction, self.D_PLUS_MEM):
            return self.memory_register_value + self.register_d.value
        elif match_bitmask(self.instruction, self.D_MINUS_MEM):
            return self.register_d.value - self.memory_register_value
        elif match_bitmask(self.instruction, self.MEM_MINUS_D):
            return self.memory_register_value - self.register_d.value
        elif match_bitmask(self.instruction, self.D_BITWISE_OR_MEM):
            return self.memory_register_value | self.register_d.value
        else:
            return self.register_d.value & self.memory_register_value

    def load_destinations(self, comp):
        if match_bitmask(self.instruction, self.DEST_M):
            self.memory_register_value = comp

        if match_bitmask(self.instruction, self.DEST_D):
            self.register_d.value = comp

        if match_bitmask(self.instruction, self.DEST_A):
            self.register_a.value = comp


    def get_next_instruction(self, comp):
        if (match_bitmask(self.instruction, self.JGT) and comp > 0) \
            or (match_bitmask(self.instruction, self.JEQ) and comp == 0) \
            or (match_bitmask(self.instruction, self.JGE) and comp >= 0) \
            or (match_bitmask(self.instruction, self.JLT) and comp < 0) \
            or (match_bitmask(self.instruction, self.JNE) and comp != 0) \
            or (match_bitmask(self.instruction, self.JLE) and comp <= 0) \
            or (match_bitmask(self.instruction, self.JMP)):
            return self.register_a.value
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
    assert h.is_load_op is False

    h = Hack(['0111111111111111'])
    assert h.is_load_op is True
