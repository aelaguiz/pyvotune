# -*- coding: utf-8 -*-

import unittest
import pyvotune

from pyvotune.util.id_generator import get_id


class TestGenome(unittest.TestCase):
    def setUp(self):
        pyvotune.set_debug(False)

    def test_assembly(self):
        @pyvotune.pint(
            range=(0, 5))
        class P1:
            def __init__(self, intparam):
                self.intparam = intparam

        @pyvotune.pbool()
        class P2:
            def __init__(self, boolparam):
                self.boolparam = boolparam

        g = pyvotune.Genome(get_id())
        g.add_gene([6], P1)
        self.assertFalse(g.assemble())

        g = pyvotune.Genome(get_id())
        g.add_gene([3], P1)
        self.assertTrue(g.assemble())

        g = pyvotune.Genome(get_id())
        g.add_gene([3], P1)
        g.add_gene([], P2)
        self.assertFalse(g.assemble())
