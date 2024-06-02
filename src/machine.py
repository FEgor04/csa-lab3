from isa import Instruction, Opcode, Addressing, read_json
from alu import ALU
from enum import Enum
import sys


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
    accumulator: int
    buffer_register: int
    address_register: int

    def __init__(
        self, input: str, _remove_later, initial_memory: list[Instruction] = []
    ):
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
            self.output += [chr(self.alu.out)]
            print("Output!!!", chr(self.alu.out))
            return
        assert 0 <= self.address_register < 2046
        self.memory[self.address_register] = Instruction(Opcode.VAR, self.alu.out)

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
            self.buffer_register = self.alu.out
        elif sel is RegisterSelector.PC:
            self.buffer_register = pc
        elif sel is RegisterSelector.ARG:
            self.buffer_register = arg
        elif sel is RegisterSelector.ADDRESS:
            self.buffer_register = address
        elif sel is RegisterSelector.OPERAND:
            self.buffer_register = operand

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

    def __init__(self, pc: int, data_path: DataPath):
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
        if (
            self.program.addressing is Addressing.IMMEDIATE
            or self.program.addressing is None
        ):
            self.operand = self.program.arg
            return
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
        if self.program.opcode is Opcode.VAR:
            raise Exception("Trying to execute VAR instruction!!!! ")
        if self.program.opcode is Opcode.HLT:
            raise StopIteration()
        if self.program.opcode is Opcode.LD:
            self.data_path.signal_latch_accumulator(
                RegisterSelector.OPERAND,
                self.program_counter,
                self.program.arg,
                self.address,
                self.operand,
            )
            self.signal_latch_pc(False)
        if self.program.opcode is Opcode.ST:
            self.data_path.signal_latch_adress_register(
                RegisterSelector.OPERAND,
                self.program_counter,
                self.program.arg,
                self.address,
                self.operand,
            )
            # Pass accumulator through the ALU
            self.data_path.alu.signal_sel_left(self.data_path.buffer_register, False)
            self.data_path.alu.signal_sel_right(self.data_path.accumulator, True)
            self.data_path.alu.signal_alu_operation(Opcode.ADD, {})
            assert (
                self.data_path.alu.out == self.data_path.accumulator
            ), "ALU out should become equal to accumulator"

            self.data_path.signal_write_memory()
            self.signal_latch_pc(False)
        elif self.program.opcode in {
            Opcode.ADD,
            Opcode.SUB,
            Opcode.MUL,
            Opcode.DIV,
            Opcode.MOD,
            Opcode.CMP,
        }:
            self.data_path.signal_latch_buffer(
                RegisterSelector.OPERAND,
                self.program_counter,
                self.program.arg,
                self.address,
                self.operand,
            )
            self.data_path.alu.signal_sel_left(self.data_path.buffer_register, True)
            self.data_path.alu.signal_sel_right(self.data_path.accumulator, True)
            self.data_path.alu.signal_alu_operation(self.program.opcode, {})
            self.data_path.signal_latch_accumulator(
                RegisterSelector.ALU,
                self.program_counter,
                self.program.arg,
                self.address,
                self.operand,
            )
            self.signal_latch_pc(False)
        elif self.program.opcode is Opcode.JMP:
            self.signal_latch_pc(True)
        elif self.program.opcode is Opcode.JZ:
            self.signal_latch_pc(self.data_path.alu.zero)

    def decode_and_execute(self):
        self.program_fetch()
        self.address_fetch()
        self.operand_fetch()
        self.execute()

    def __repr__(self):
        return f"{self.program_counter:6d} | {self.data_path.accumulator:6d} | {self.data_path.buffer_register:6d} | {self.data_path.address_register:6d}"


def simulate(instructions: list[Instruction], pc, input) -> str:
    data_path = DataPath(input, 0, instructions)
    control_unit = ControlUnit(pc, data_path)
    try:
        for i in range(1000000):
            print(f"instruction #{i}")
            control_unit.decode_and_execute()
            print(control_unit.__repr__())
    except StopIteration:
        print("HLT!")
    except EOFError:
        print("Programm tried to read empty input")
    return "".join(data_path.output)


if __name__ == "__main__":
    assert len(sys.argv) == 3, "Wrong arguments: machine.py <code_file> <input_file>"
    _, code_file, input_file = sys.argv
    with open(code_file, "r") as f:
        instructions, pc = read_json(f.read())
    output = simulate(instructions, pc, "")
    print(output)
