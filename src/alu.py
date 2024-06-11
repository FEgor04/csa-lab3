from __future__ import annotations

from enum import Enum
from typing import Callable

from isa import Opcode

operations: dict[Opcode, Callable[[int, int], int]] = {
    Opcode.ADD: lambda x, y: x + y,
    Opcode.SUB: lambda x, y: x - y,
    Opcode.MUL: lambda x, y: x * y,
    Opcode.DIV: lambda x, y: x // y,
    Opcode.MOD: lambda x, y: x % y,
    Opcode.CMP: lambda x, y: x - y,
}


class ALUModifier(int, Enum):
    NegLeft = 0
    NegRight = 1
    IncLeft = (2,)
    IncRight = 3
    DecLeft = 4
    DecRight = 5


class ALU:
    right = 0
    left = 0
    out = 0
    negative = False
    zero = True

    def __init__(self):
        pass

    def signal_sel_left(self, buffer: int, signal: bool):
        self.left = buffer if signal else 0

    def signal_sel_right(self, accumulator: int, signal: bool):
        self.right = accumulator if signal else 0

    def process_modifiers(self, modifiers: set[ALUModifier]) -> tuple[int, int]:
        left = self.left
        right = self.right

        if ALUModifier.NegLeft in modifiers:
            left *= -1
        if ALUModifier.NegRight in modifiers:
            right *= -1
        if ALUModifier.IncLeft in modifiers:
            left += 1
        if ALUModifier.DecLeft in modifiers:
            left -= 1
        if ALUModifier.IncRight in modifiers:
            right += 1
        if ALUModifier.DecRight in modifiers:
            right -= 1
        return left, right

    def signal_alu_operation(self, operation: Opcode, modifiers: set[ALUModifier]):
        left, right = self.process_modifiers(modifiers)
        out = operations[operation](right, left)
        if operation is not Opcode.CMP:
            self.out = out
        self.negative = out < 0
        self.zero = out == 0
