from isa import Instruction, Opcode, Addressing
from alu import ALU
from enum import Enum


class RegisterSelector(Enum):
    ALU = "alu"
    MEM = "mem"
    # Аргумент инструкции
    ARG = "argument"


class AddressRegisterSelector(Enum):
    ALU = "alu"
    PC = "pc"
    ARG = "arg"
    # Адрес операнда, полученный после цикла Address Fetch
    ADDRESS = "address"


class DataPath:
    def __init__(self, input: str, onOutput, initial_memory: list[Instruction] = []):
        """
        Для простоты реализации в памяти хранятся инструкции.
        чтобы сохранить число необходимо указать `Opcode.VAR` и `Addressing.Immediate`
        """
        self.memory = [Instruction(Opcode.VAR, 0, Addressing.IMMEDIATE)] * 2046

        for i in range(len(initial_memory)):
            self.memory[i] = initial_memory[i]

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

    def signal_latch_adress_register(
        self, sel: AddressRegisterSelector, pc: int, arg: int, address: int
    ):
        if sel is AddressRegisterSelector.ALU:
            self.address_register = self.alu.out
        elif sel is AddressRegisterSelector.PC:
            self.address_register = pc
        elif sel is AddressRegisterSelector.ARG:
            self.address_register = arg
        elif sel is AddressRegisterSelector.ADDRESS:
            self.address_register = address

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


class ControlUnit:
    program: Instruction
    program_counter: int
    data_path: DataPath

    address: int
    operand: int

    def __init__(self, pc, data_path):
        self.program = None
        self.program_counter = pc
        self.data_path = data_path
        self.address = None
        self.operand = None

    def signal_latch_pc(self, sel: bool, operand: int):
        self.program_counter = operand if sel else self.program_counter + 1

    def program_fetch(self):
        self.data_path.signal_latch_adress_register(
            "pc",
            self.program_counter,
            self.program.arg if self.program is not None else 0,
            self.address,
        )
        self.data_path.signal_read_memory()
        self.program = self.data_path.mem_out

    def address_fetch(self):
        assert self.program is not None
        if self.program.addressing is Addressing.IMMEDIATE:
            return
        if self.program.addressing is Addressing.DIRECT:
            self.address = self.program.arg
        if self.program.addressing is Addressing.INDIRECT:
            self.data_path.signal_latch_adress_register(
                AddressRegisterSelector.ARG,
                self.program_counter,
                self.program.arg,
                self.address,
            )
            self.data_path.signal_read_memory()
            self.address = self.data_path.mem_out.arg
