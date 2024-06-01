from isa import Instruction, Opcode, Addressing
from enum import Enum


class ALUOperation(int, Enum):
    Add = 0
    Sub = 1


class DataPath:
    def __init__(self, input: str):
        """
        Для простоты реализации в памяти хранятся инструкции.
        чтобы сохранить число необходимо указать `Opcode.VAR` и `Addressing.Immediate`
        """
        self.memory = [Instruction(Opcode.VAR, 0, Addressing.IMMEDIATE)] * 2046
        self.address_register = 0
        self.accumulator = 0
        self.buffer_register = 0
        self.input = input
        self.output = []
        self.alu_out = 0
        self.mem_out = 0

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
