from isa import Instruction, Opcode
from translator import parse_lines, parse_labels, split_instruction
import unittest


class TestTranslator(unittest.TestCase):
    def test_translate_no_arg(self):
        lines = ["HLT", "", ""]
        transformed = parse_lines(lines)
        expected = [Instruction(Opcode.HLT, None)]
        self.assertEqual(transformed, expected)

    def test_translate_complex(self):
        lines = ["START: LD KEKW", "JMP START", "KEKW: VAR 'a'"]
        transformed = parse_lines(lines)
        expected = [
            Instruction(Opcode.LD, 2),
            Instruction(Opcode.JMP, 0),
            Instruction(Opcode.VAR, "'a'"),
        ]
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

    def test_parse_instruction_no_arg(self):
        line = "\t\tKEKW:\t\tHLT\t\t\t\t"
        expected = ("KEKW", "HLT", "")
        self.assertEqual(split_instruction(line), expected)

    def test_parse_instruction_no_arg_no_label(self):
        line = "\t\t\tHLT\t\t\t\t"
        expected = ("", "HLT", "")
        self.assertEqual(split_instruction(line), expected)

    def test_parse_instruction(self):
        line = "\t\tCOOLLABEL: \tADD\t\tSOMETHING\t\t\t\n"
        expected = ("COOLLABEL", "ADD", "SOMETHING")
        self.assertEqual(split_instruction(line), expected)
