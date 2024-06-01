from isa import Instruction, Opcode, Addressing
from machine import DataPath, ControlUnit
import unittest


class ControlUnitTest(unittest.TestCase):
    def test_program_fetch(self):
        initial = [Instruction(Opcode.LD, 50, Addressing.IMMEDIATE)]
        data_path = DataPath("", print, initial)
        control_unit = ControlUnit(0, data_path)
        control_unit.program_fetch()
        self.assertEqual(initial[0], control_unit.program)

    def test_address_fetch_direct(self):
        initial = [Instruction(Opcode.LD, 50, Addressing.DIRECT)]
        data_path = DataPath("", print, initial)
        control_unit = ControlUnit(0, data_path)
        control_unit.program_fetch()
        control_unit.address_fetch()
        self.assertEqual(50, control_unit.address)

    def test_address_fetch_indirect(self):
        initial = [
            Instruction(Opcode.LD, 1, Addressing.INDIRECT),
            Instruction(Opcode.VAR, 512, Addressing.IMMEDIATE),
        ]
        data_path = DataPath("", print, initial)
        control_unit = ControlUnit(0, data_path)
        control_unit.program_fetch()
        control_unit.address_fetch()
        self.assertEqual(512, control_unit.address)
