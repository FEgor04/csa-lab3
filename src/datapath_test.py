from machine import DataPath

import unittest


class DataPathTest(unittest.TestCase):
    def test_read_input(self):
        datapath = DataPath("kek")
        datapath.address_register = 2046
        actual = list(
            map(
                lambda i: i.arg,
                [
                    datapath.read_memory(),
                    datapath.read_memory(),
                    datapath.read_memory(),
                ],
            )
        )
        expected = list(map(lambda c: ord(c), ["k", "e", "k"]))
        self.assertEqual(expected, actual)
