from machine import DataPath

import unittest


class DataPathTest(unittest.TestCase):
    def test_read_input(self):
        datapath = DataPath("kek")
        datapath.address_register = 2046
        datapath.signal_read_memory()
        self.assertEqual(ord("k"), datapath.mem_out.arg)
        datapath.signal_read_memory()
        self.assertEqual(ord("e"), datapath.mem_out.arg)
        datapath.signal_read_memory()
        self.assertEqual(ord("k"), datapath.mem_out.arg)
        self.assertRaises(EOFError, datapath.signal_read_memory)
