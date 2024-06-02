import unittest
from translator import parse_lines
from machine import DataPath, ControlUnit, simulate


class IntegrationTest(unittest.TestCase):
    def test_sum(self):
        lines = ["RESULT: VAR 0", "START: LD 5", "ADD 10", "ST RESULT", "HLT"]
        instructions, pc = parse_lines(lines)
        data_path = DataPath("", print, instructions)
        control_unit = ControlUnit(pc, data_path)
        try:
            for i in range(10):
                control_unit.decode_and_execute()
        except StopIteration:
            pass
        self.assertEqual(data_path.memory[0].arg, 10 + 5)

    def test_mul_input(self):
        lines = [
            "RESULT: VAR 0",
            "START: LD (2046)",
            "SUB '0'",
            "MUL 10",
            "ST RESULT",
            "HLT",
        ]
        instructions, pc = parse_lines(lines)
        data_path = DataPath("5", print, instructions)
        control_unit = ControlUnit(pc, data_path)
        try:
            for i in range(100):
                control_unit.decode_and_execute()
        except StopIteration:
            pass
        self.assertEqual(data_path.memory[0].arg, 50)

    def test_output(self):
        lines = ["START: LD 'h'", "ST 2047", "HLT"]
        instructions, pc = parse_lines(lines)
        data_path = DataPath("", print, instructions)
        control_unit = ControlUnit(pc, data_path)
        try:
            for i in range(100):
                control_unit.decode_and_execute()
        except StopIteration:
            pass
        self.assertEqual(data_path.output, ["h"])

    def test_hello_world(self):
        lines = [
            "HELLO: VAR 'hello, world'",
            "I: VAR HELLO",
            "START: LD [I]",
            "ST 2047",
            "CMP 0",
            "JZ STOP",
            "LD (I)",
            "ADD 1",
            "ST I",
            "JMP START",
            "STOP: HLT",
        ]
        instructions, pc = parse_lines(lines)
        output = simulate(instructions, pc, "")
        self.assertEqual("hello, world\0", output)
