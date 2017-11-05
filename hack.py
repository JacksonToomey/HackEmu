from ram import Ram
from rom import Rom
from register import Register


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
    CONSTANT_ONE = 4032
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

    INSTR_MASK = 4032
    JUMP_MASK = 7
    DEST_MASK = 56
    A_INSTR_MASK = 0x8000
    LOAD_MASK = 4096

    def __init__(self, data=None, fromq=None, toq=None):
        self.ram = Ram(32768, fromq, toq)
        self.rom = Rom(32768, data=data)
        self.register_a = Register()
        self.register_d = Register()
        self.program_counter = Register()

    def execute(self):
        if self.c_instruction:
            d = self.register_d.value
            if self.from_ram:
                mem = self.ram[self.register_a.value]
            else:
                mem = self.register_a.value
            comp = self.get_comp(d, mem)
            self.store_value(comp)
            self.program_counter.value = self.get_next(comp)
        else:
            self.register_a.value = self.instruction
            self.program_counter.value = self.program_counter.value + 1
        self.ram.update_key_buffer()

    def get_comp(self, d, mem):
        if self.op == self.CONSTANT_ZERO:
            return 0
        elif self.op == self.CONSTANT_ONE:
            return 1
        elif self.op == self.CONSTANT_NEG_ONE:
            return -1
        elif self.op == self.D_REG:
            return d
        elif self.op == self.MEM_REG:
            return mem
        elif self.op == self.NOT_D:
            return ~d
        elif self.op == self.NOT_MEM:
            return ~mem
        elif self.op == self.NEG_D:
            return -1 * d
        elif self.op == self.NEG_MEM:
            return -1 * mem
        elif self.op == self.INCR_D:
            return d + 1
        elif self.op == self.INCR_MEM:
            return mem + 1
        elif self.op == self.DEC_D:
            return d - 1
        elif self.op == self.DEC_MEM:
            return mem - 1
        elif self.op == self.D_PLUS_MEM:
            return mem + d
        elif self.op == self.D_MINUS_MEM:
            return d - mem
        elif self.op == self.MEM_MINUS_D:
            return mem - d
        elif self.op == self.D_BITWISE_OR_MEM:
            return mem | d
        else:
            return d & mem

    def store_value(self, comp):
        if self.store_m:
            self.ram[self.register_a.value] = comp
        if self.store_d:
            self.register_d.value = comp
        if self.store_a:
            self.register_a.value = comp

    def get_next(self, comp):
        jump = False
        if self.jump == 1 and comp > 0:
            jump = True
        elif self.jump == 2 and comp == 0:
            jump = True
        elif self.jump == 3 and comp >= 0:
            jump = True
        elif self.jump == 4 and comp < 0:
            jump = True
        elif self.jump == 5 and comp != 0:
            jump = True
        elif self.jump == 6 and comp <= 0:
            jump = True
        elif self.jump == 7:
            jump = True

        if jump:
            return self.register_a.value
        else:
            return self.program_counter.value + 1

    @property
    def instruction(self):
        return self.rom[self.program_counter.value]

    @property
    def c_instruction(self):
        return (self.instruction & 0x8000) == 0x8000

    @property
    def from_ram(self):
        return (self.instruction & 0x1000) == 0x1000

    @property
    def op(self):
        return self.instruction & 0xFC0

    @property
    def dest(self):
        return self.instruction & 0x38

    @property
    def jump(self):
        return self.instruction & 0x7

    @property
    def store_m(self):
        return (self.dest & 0x8) == 0x8

    @property
    def store_d(self):
        return (self.dest & 0x10) == 0x10

    @property
    def store_a(self):
        return (self.dest & 0x20) == 0x20
