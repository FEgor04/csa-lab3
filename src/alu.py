from enum import Enum


class ALUOperation(int, Enum):
    Add = 0
    Sub = 1


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

    def signal_alu_operation(
        self, operation: ALUOperation, modifiers: set[ALUModifier]
    ):
        left, right = self.process_modifiers(modifiers)
        if operation is ALUOperation.Add:
            self.out = left + right
        if operation is ALUOperation.Sub:
            self.out = right - left  # accumulator - left
        self.negative = self.out < 0
        self.zero = self.out == 0
