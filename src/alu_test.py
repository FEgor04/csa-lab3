import unittest

from alu import ALU, ALUModifier
from isa import Opcode


class TestTranslator(unittest.TestCase):
    def test_inc_left(self):
        alu = ALU()
        alu.signal_sel_left(0, 0)
        alu.signal_sel_right(0, 0)
        alu.signal_alu_operation(Opcode.ADD, set([ALUModifier.IncLeft]))
        assert 1 == alu.out

    def test_inc_left_dec_right(self):
        alu = ALU()
        alu.signal_sel_left(1, True)
        alu.signal_sel_right(-1, True)
        # -2 - 2
        alu.signal_alu_operation(Opcode.SUB, set([ALUModifier.IncLeft, ALUModifier.DecRight]))
        assert -4 == alu.out
