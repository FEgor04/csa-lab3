from isa import Instruction, Opcode, Addressing
from alu import ALU, ALUOperation
from enum import Enum


class RegisterSelector(Enum):
    ALU = "alu"
    MEM = "mem"
    PC = "pc"
    # Аргумент инструкции
    ARG = "arg"
    # Адрес операнда, полученный после цикла Address Fetch
    ADDRESS = "address"
    # Операнд после цикла Operand Fetch
    OPERAND = "operand"


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
        self, sel: RegisterSelector, pc: int, arg: int, address: int, operand: int
    ):
        if sel is RegisterSelector.ALU:
            self.address_register = self.alu.out
        elif sel is RegisterSelector.PC:
            self.address_register = pc
        elif sel is RegisterSelector.ARG:
            self.address_register = arg
        elif sel is RegisterSelector.ADDRESS:
            self.address_register = address
        elif sel is RegisterSelector.OPERAND:
            self.address_register = operand

    def signal_latch_buffer(
        self, sel: RegisterSelector, pc: int, arg: int, address: int, operand: int
    ):
        if sel is RegisterSelector.ALU:
            self.buffer = self.alu.out
        elif sel is RegisterSelector.PC:
            self.buffer = pc
        elif sel is RegisterSelector.ARG:
            self.buffer = arg
        elif sel is RegisterSelector.ADDRESS:
            self.buffer = address
        elif sel is RegisterSelector.OPERAND:
            self.buffer = operand

    def signal_latch_accumulator(
        self, sel: RegisterSelector, pc: int, arg: int, address: int, operand: int
    ):
        if sel is RegisterSelector.ALU:
            self.accumulator = self.alu.out
        elif sel is RegisterSelector.PC:
            self.accumulator = pc
        elif sel is RegisterSelector.ARG:
            self.accumulator = arg
        elif sel is RegisterSelector.ADDRESS:
            self.accumulator = address
        elif sel is RegisterSelector.OPERAND:
            self.accumulator = operand


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

    def signal_latch_pc(self, sel: bool):
        self.program_counter = self.operand if sel else self.program_counter + 1

    def program_fetch(self):
        self.data_path.signal_latch_adress_register(
            RegisterSelector.PC,
            self.program_counter,
            self.program.arg if self.program is not None else 0,
            self.address,
            self.operand,
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
                RegisterSelector.ARG,
                self.program_counter,
                self.program.arg,
                self.address,
                self.operand,
            )
            self.data_path.signal_read_memory()
            self.address = self.data_path.mem_out.arg

    def operand_fetch(self):
        assert self.program is not None
        if self.program.addressing is Addressing.IMMEDIATE:
            self.operand = self.program.arg
            return
        assert self.address is not None
        self.data_path.signal_latch_adress_register(
            RegisterSelector.ADDRESS,
            self.program_counter,
            self.program.arg if self.program is not None else 0,
            self.address,
            self.operand,
        )
        self.data_path.signal_read_memory()
        self.operand = self.data_path.mem_out.arg

    def execute(self):
        if self.program.opcode is Opcode.LD:
            self.data_path.signal_latch_accumulator(
                RegisterSelector.OPERAND,
                self.program_counter,
                self.program.arg,
                self.address,
                self.operand,
            )
            self.signal_latch_pc(False)
        elif self.program.opcode is Opcode.ADD:
            print("executing add")
            self.data_path.signal_latch_buffer(
                RegisterSelector.OPERAND,
                self.program_counter,
                self.program.arg,
                self.address,
                self.operand,
            )
            self.data_path.alu.signal_sel_left(self.data_path.buffer, True)
            self.data_path.alu.signal_sel_right(self.data_path.accumulator, True)
            self.data_path.alu.signal_alu_operation(ALUOperation.Add, {})
            self.data_path.signal_latch_accumulator(
                RegisterSelector.ALU,
                self.program_counter,
                self.program.arg,
                self.address,
                self.operand,
            )
            self.signal_latch_pc(False)

    def decode_and_execute(self):
        self.program_fetch()
        self.address_fetch()
        self.operand_fetch()
        self.execute()
