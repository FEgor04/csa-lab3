import unittest
from translator import parse_lines
from machine import DataPath, ControlUnit


class IntegrationTest(unittest.TestCase):
    def test_sum(self):
        lines = ["RESULT: VAR 0", "LD 5", "ADD 10", "ST RESULT", "HLT"]
        instructions = parse_lines(lines)
        data_path = DataPath("", print, instructions)
        control_unit = ControlUnit(1, data_path)
        try:
            for i in range(10):
                control_unit.decode_and_execute()
        except StopIteration:
            pass
        self.assertEqual(data_path.memory[0].arg, 10 + 5)

    def test_mul_input(self):
        lines = ["RESULT: VAR 0", "LD (2046)", "SUB '0'", "MUL 10", "ST RESULT", "HLT"]
        instructions = parse_lines(lines)
        data_path = DataPath("5", print, instructions)
        control_unit = ControlUnit(1, data_path)
        try:
            for i in range(100):
                control_unit.decode_and_execute()
        except StopIteration:
            pass
        self.assertEqual(data_path.memory[0].arg, 50)

    def test_output(self):
        lines = ["LD 'h'", "ST 2047", "HLT"]
        instructions = parse_lines(lines)
        data_path = DataPath("", print, instructions)
        control_unit = ControlUnit(0, data_path)
        try:
            for i in range(100):
                control_unit.decode_and_execute()
        except StopIteration:
            pass
        self.assertEqual(data_path.output, ["h"])
