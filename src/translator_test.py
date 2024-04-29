from isa import Instruction, Opcode
from translator import parse_lines, parse_labels, split_instruction
import unittest

class TestTranslator(unittest.TestCase):
    @unittest.skip("TBD")
    def test_translate_no_arg(self):
        lines = ["HLT"]
        transformed = parse_lines(lines)
        expected = [Instruction(Opcode.HLT, None)]
        self.assertEqual(transformed, expected)

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
        self.assertEqual(actual, expected_labels)


    def test_parse_instruction_no_label(self):
        line = "\t\t\tLD\t\tABSD\t\t"
        expected = ("", "LD", "ABSD")
        self.assertEqual(split_instruction(line), expected)
        
