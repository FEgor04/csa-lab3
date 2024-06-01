from alu import ALU, ALUModifier, ALUOperation
import unittest


class TestTranslator(unittest.TestCase):
    def test_inc_left(self):
        alu = ALU()
        alu.signal_sel_left(0, 0)
        alu.signal_sel_right(0, 0)
        alu.signal_alu_operation(ALUOperation.Add, set([ALUModifier.IncLeft]))
        self.assertEqual(1, alu.out)

    def test_inc_left_dec_right(self):
        alu = ALU()
        alu.signal_sel_left(1, True)
        alu.signal_sel_right(-1, True)
        # -2 - 2
        alu.signal_alu_operation(
            ALUOperation.Sub, set([ALUModifier.IncLeft, ALUModifier.DecRight])
        )
        self.assertEqual(-4, alu.out)
