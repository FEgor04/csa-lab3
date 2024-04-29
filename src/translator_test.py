from isa import Instruction, Opcode
from translator import parse_lines, parse_labels
import unittest

class TestTranslator(unittest.TestCase):
    @unittest.skip("TBD")
    def test_translate_no_arg(self):
        lines = ["HLT"]
        transformed = parse_lines(lines)
        expected = [Instruction(Opcode.HLT, None)]
        self.assertEquals(transformed, expected)

    def test_first_pass(self):
        lines = [
            "LABEL1: HLT",
            "LABEL2: JMP LABEL1",
        ]
        expected_labels = {
            "LABEL1": 0,
            "LABEL2": 1,
        }
        actual = parse_labels(lines)
        self.assertEquals(actual, expected_labels)

