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
