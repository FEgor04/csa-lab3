from __future__ import annotations

import sys
from enum import Enum

from alu import ALU
from isa import Addressing, Instruction, Opcode, is_arithmetic_instruction, read_json


class RegisterSelector(Enum):
    ALU = "alu"
    MEM = "mem"
    PC = "pc"

class DataPath:
    accumulator: int
    buffer_register: int
    address_register: int

    def __init__(self, input_str: str, _remove_later, initial_memory: list[Instruction] = []):
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
        self.input = input_str
        self.output = []
        self.mem_out = 0
        self.alu = ALU()

    def signal_read_memory(self) -> Instruction:
        assert self.address_register != 2047, "program tried to read from output port"
        if self.address_register == 2046:  # Input
            if len(self.input) == 0:
                raise EOFError()
            symbol = ord(self.input[0])
            self.input = self.input[1:]
            self.mem_out = Instruction(Opcode.VAR, symbol, Addressing.IMMEDIATE)
            return
        assert 0 <= self.address_register < 2046
        self.mem_out = self.memory[self.address_register]

    def signal_write_memory(self):
        assert self.address_register != 2046, "program tried to write to input port"
        if self.address_register == 2047:
            char = chr(self.alu.out)
            self.output += [char]
            return
        assert 0 <= self.address_register < 2046
        self.memory[self.address_register] = Instruction(Opcode.VAR, self.alu.out)

    def signal_latch_address_register(self, sel: RegisterSelector, pc: int):
        if sel is RegisterSelector.ALU:
            self.address_register = self.alu.out
        elif sel is RegisterSelector.PC:
            self.address_register = pc
        elif sel is RegisterSelector.MEM:
            self.address_register = self.mem_out.arg

    def signal_latch_buffer(self, sel: RegisterSelector, pc: int):
        if sel is RegisterSelector.ALU:
            self.buffer_register = self.alu.out
        elif sel is RegisterSelector.PC:
            self.buffer_register = pc
        elif sel is RegisterSelector.MEM:
            self.buffer_register = self.mem_out.arg

    def signal_latch_accumulator(self, sel: RegisterSelector, pc: int):
        if sel is RegisterSelector.ALU:
            self.accumulator = self.alu.out
        elif sel is RegisterSelector.PC:
            self.accumulator = pc
        elif sel is RegisterSelector.MEM:
            self.accumulator = self.mem_out.arg
        

class ControlUnit:
    program: Instruction
    program_counter: int
    data_path: DataPath

    address: int
    operand: int

    _tick: int = 0
    _instruction_number: int = 0

    def tick(self):
        self._tick += 1

    def get_current_tick(self) -> int:
        return self._tick

    def get_instruction_number(self) -> int:
        return self._instruction_number

    def __init__(self, pc: int, data_path: DataPath):
        self.program = None
        self.program_counter = pc
        self.data_path = data_path

    def signal_latch_pc(self, sel: bool):
        self.program_counter = self.data_path.mem_out.arg if sel else self.program_counter + 1

    def signal_latch_address_register(self, sel: RegisterSelector):
        self.data_path.signal_latch_address_register(sel, self.program_counter)

    def signal_latch_buffer(self, sel: RegisterSelector):
        self.data_path.signal_latch_buffer(sel, self.program_counter)

    def signal_latch_accumulator(self, sel: RegisterSelector):
        self.data_path.signal_latch_accumulator(sel, self.program_counter)

    def signal_latch_program(self):
        self.program = self.data_path.mem_out

    def program_fetch(self):
        self.signal_latch_address_register(
            RegisterSelector.PC,
        )
        self.data_path.signal_read_memory()
        self.signal_latch_program()
        self.tick()

    def address_fetch(self):
        """
        Цикл получения адреса операнда.
        До него в program лежит текущая программа
        После него AR содержит адрес операнда текущей инструкции.
        """
        assert self.program is not None
        if self.program.addressing is Addressing.IMMEDIATE:
            return
        if self.program.addressing is Addressing.DIRECT:
            self.signal_latch_address_register(RegisterSelector.MEM)
        if self.program.addressing is Addressing.INDIRECT:
            self.signal_latch_address_register(RegisterSelector.MEM)
            self.data_path.signal_read_memory()
            self.tick()
            self.signal_latch_address_register(RegisterSelector.MEM)

    def operand_fetch(self):
        """
        Цикл получения операнда.
        До него адрес операнда лежит в AR.
        После него MEM_OUT содержит операнд текущей инструкции.
        """
        assert self.program is not None
        if self.program.addressing is Addressing.IMMEDIATE or self.program.addressing is None:
            return
        self.data_path.signal_read_memory()
        self.tick()

    def _execute_ld(self):
        self.signal_latch_accumulator(
            RegisterSelector.MEM,
        )
        self.signal_latch_pc(False)
        self.tick()

    def _execute_arithmetic(self):
        self.signal_latch_buffer(
            RegisterSelector.MEM,
        )
        self.data_path.alu.signal_sel_left(self.data_path.buffer_register, True)
        self.data_path.alu.signal_sel_right(self.data_path.accumulator, True)
        self.data_path.alu.signal_alu_operation(self.program.opcode, {})
        if self.program.opcode is not Opcode.CMP:
            self.signal_latch_accumulator(
                RegisterSelector.ALU,
            )
        self.signal_latch_pc(False)
        self.tick()

    def _execute_st(self):
        self.signal_latch_address_register(
            RegisterSelector.MEM,
        )
        # Pass accumulator through the ALU
        self.data_path.alu.signal_sel_left(self.data_path.buffer_register, False)
        self.data_path.alu.signal_sel_right(self.data_path.accumulator, True)
        self.data_path.alu.signal_alu_operation(Opcode.ADD, {})
        self.data_path.signal_write_memory()
        self.signal_latch_pc(False)
        self.tick()

    def execute(self):
        assert self.program.opcode is not Opcode.VAR, "program tried to execute VAR instruction"
        if self.program.opcode is Opcode.HLT:
            raise StopIteration()
        if self.program.opcode is Opcode.LD:
            self._execute_ld()
        if self.program.opcode is Opcode.ST:
            self._execute_st()
        elif is_arithmetic_instruction(self.program.opcode):
            self._execute_arithmetic()
        elif self.program.opcode is Opcode.JMP:
            self.signal_latch_pc(True)
            self.tick()
        elif self.program.opcode is Opcode.JZ:
            self.signal_latch_pc(self.data_path.alu.zero)
            self.tick()

    def decode_and_execute(self):
        self.program_fetch()
        self.address_fetch()
        self.operand_fetch()
        self.execute()
        self._instruction_number += 1

    def __repr__(self):
        return f"{self.program_counter:6d} | {self.data_path.accumulator:6d} | {self.data_path.buffer_register:6d} | {self.data_path.address_register:6d} | {self.get_instruction_number():6d} | {self.get_current_tick():6d}"


def simulate(instructions: list[Instruction], pc, input_text) -> tuple[str, DataPath, ControlUnit]:
    data_path = DataPath(input_text, 0, instructions)
    control_unit = ControlUnit(pc, data_path)
    try:
        for i in range(1000000):
            control_unit.decode_and_execute()
            print(control_unit.__repr__())
    except StopIteration:
        print("Program haulted successfully")
    except EOFError:
        print("Program tried to read empty input")
    return "".join(data_path.output), data_path, control_unit


if __name__ == "__main__":
    assert len(sys.argv) == 3, "Wrong arguments: machine.py <code_file> <input_file>"
    _, code_file, input_file = sys.argv
    with open(input_file) as f:
        input_text = f.read()
        input_text += "\0"
    with open(code_file) as f:
        instructions, pc = read_json(f.read())
    output, _, _ = simulate(instructions, pc, input_text)
    print(output)
