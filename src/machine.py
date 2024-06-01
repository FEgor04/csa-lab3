from isa import Instruction, Opcode, Addressing
from alu import ALU
from enum import Enum


class RegisterSelector(Enum):
    ALU = "alu"
    MEM = "mem"
    # Аргумент инструкции
    ARG = "argument"


class DataPath:
    def __init__(self, input: str, onOutput):
        """
        Для простоты реализации в памяти хранятся инструкции.
        чтобы сохранить число необходимо указать `Opcode.VAR` и `Addressing.Immediate`
        """
        self.memory = [Instruction(Opcode.VAR, 0, Addressing.IMMEDIATE)] * 2046
        self.address_register: int = 0
        self.accumulator: int = 0
        self.buffer_register: int = 0
        self.input = input
        self.output = []
        self.mem_out = 0
        self.alu = ALU()

    def signal_read_memory(self) -> Instruction:
        if self.address_register == 2046:  # Input
            if len(self.input) == 0:
                raise EOFError()
            symbol = ord(self.input[0])
            self.input = self.input[1:]
            self.mem_out = Instruction(Opcode.VAR, symbol, Addressing.IMMEDIATE)
            return
        if self.address_register == 2047:
            raise Exception("Programm tried to read from output port")
        assert 0 <= self.address_register < 2046
        self.mem_out = self.memory[self.address_register]

    def signal_write_memory(self):
        if self.address_register == 2046:
            raise Exception("Programm tried to write to input port")
        if self.address_register == 2047:
            self.onOutput(self.alu.out)
            return
        assert 0 <= self.address_register < 2046
        self.memory[self.address_register] = self.alu.out

    def signal_latch_adress_register(self, sel: str | None, pc: int):
        if sel == "alu":
            self.address_register = self.alu.out
        elif sel == "pc":
            self.address_register = pc
        else:
            self.address_register = 0

    def signal_latch_buffer(self, sel: RegisterSelector, argument: int):
        if sel is RegisterSelector.ALU:
            self.buffer = self.alu.out
        if sel is RegisterSelector.MEM:
            self.buffer = self.mem_out
        if sel is RegisterSelector.ARG:
            self.buffer = self.argument

    def signal_latch_accumulator(self, sel: RegisterSelector, argument: int):
        if sel is RegisterSelector.ALU:
            self.accumulator = self.alu.out
        if sel is RegisterSelector.MEM:
            self.accumulator = self.mem_out
        if sel is RegisterSelector.ARG:
            self.accumulator = self.argument
