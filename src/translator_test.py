from isa import Instruction, Opcode
from translator import parse_lines
import unittest

class TestTranslator(unittest.TestCase):
    def test_translate_no_arg(self):
        lines = ["HLT"]
        transformed = parse_lines(lines)
        expected = [Instruction(Opcode.HLT, None)]
        self.assertEquals(transformed, expected)
