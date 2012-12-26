# -*- coding: utf-8 -*-

import unittest
import pyvotune


class TestGenome(unittest.TestCase):
    def test_general(self):
        @pyvotune.int(
            range=(0, 5))
        class P1:
            def __init__(self, intparam):
                self.intparam = intparam

        @pyvotune.bool()
        class P2:
            def __init__(self, boolparam):
                self.boolparam = boolparam

        g = pyvotune.Genome(
