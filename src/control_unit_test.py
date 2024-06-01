from isa import Instruction, Opcode, Addressing
from machine import DataPath, ControlUnit
import unittest

class ControlUnitTest(unittest.TestCase):
    def test_program_fetch(self):
        initial = [
            Instruction(Opcode.LD, 50, Addressing.IMMEDIATE)
        ]
        data_path = DataPath("", print, initial)
        control_unit = ControlUnit(0, data_path)
        control_unit.program_fetch()
        self.assertEqual(initial[0], control_unit.program)
        
