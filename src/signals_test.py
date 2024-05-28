import unittest
from machine import Signal

class TestSignal(unittest.TestCase):
    def test_are_power_of_two(self):
        signals = [Signal.SEL_BUFFER_IN_ALU_OUT, Signal.SEL_BUFFER_IN_MEM_OUT, Signal.LATCH_BUFFER]
        self.assertEqual(signals, [1, 2, 4])
