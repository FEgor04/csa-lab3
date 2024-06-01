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

    def test_operand_fetch_immediate(self):
        initial = [
            Instruction(Opcode.LD, 50, Addressing.IMMEDIATE),
        ]
        data_path = DataPath("", print, initial)
        control_unit = ControlUnit(0, data_path)
        control_unit.program_fetch()
        control_unit.address_fetch()
        control_unit.operand_fetch()
        self.assertEqual(50, control_unit.operand)

    def test_operand_fetch_direct(self):
        initial = [
            Instruction(Opcode.LD, 1, Addressing.DIRECT),
            Instruction(Opcode.VAR, 512, Addressing.IMMEDIATE),
        ]
        data_path = DataPath("", print, initial)
        control_unit = ControlUnit(0, data_path)
        control_unit.program_fetch()
        control_unit.address_fetch()
        control_unit.operand_fetch()
        self.assertEqual(512, control_unit.operand)

    def test_operand_fetch_indirect(self):
        initial = [
            Instruction(Opcode.LD, 1, Addressing.INDIRECT),
            Instruction(Opcode.VAR, 2, Addressing.IMMEDIATE),
            Instruction(Opcode.VAR, 512, Addressing.IMMEDIATE),
        ]
        data_path = DataPath("", print, initial)
        control_unit = ControlUnit(0, data_path)
        control_unit.program_fetch()
        control_unit.address_fetch()
        control_unit.operand_fetch()
        self.assertEqual(512, control_unit.operand)

    def test_execute_load(self):
        initial = [
            Instruction(Opcode.LD, 42, Addressing.IMMEDIATE),
        ]
        data_path = DataPath("", print, initial)
        control_unit = ControlUnit(0, data_path)
        control_unit.program_fetch()
        control_unit.address_fetch()
        control_unit.operand_fetch()
        control_unit.execute()
        self.assertEqual(42, data_path.accumulator)

    def test_execute_add(self):
        initial = [
            Instruction(Opcode.LD, 42, Addressing.IMMEDIATE),
            Instruction(Opcode.ADD, 42, Addressing.IMMEDIATE),
        ]
        data_path = DataPath("", print, initial)
        control_unit = ControlUnit(0, data_path)
        control_unit.decode_and_execute()
        self.assertEqual(1, control_unit.program_counter)
        control_unit.decode_and_execute()
        self.assertEqual(2, control_unit.program_counter)
        self.assertEqual(84, data_path.accumulator)
