# -*- coding: utf-8 -*-

import unittest
import pyvotune
import random

from pyvotune.util.id_generator import get_id


class TestMutators(unittest.TestCase):
    def setUp(self):
        pyvotune.set_debug(False)

    def test_random_reset(self):
        @pyvotune.pint(
            range=(0, 5))
        class P1:
            def __init__(self, intparam):
                self.intparam = intparam

        g1 = pyvotune.Genome(get_id())
        g1.add_gene([3], P1)
        self.assertTrue(g1.assemble())

        r = random.Random()

        prev_val = g1[0][1]
        some_diff = False
        for i in range(100):
            (g2,) = pyvotune.variators.param_reset_mutation(
                r, [g1], {'mutation_rate': 1.0})
            new_val = g2[0][1]
            if new_val != prev_val:
                some_diff = True
            self.assertTrue(new_val >= 0 and new_val < 5)

        self.assertTrue(some_diff)

    def test_scramble_mutation(self):
        @pyvotune.pint(
            range=(0, 5))
        class P1:
            def __init__(self, intparam):
                self.intparam = intparam

        g1 = pyvotune.Genome(get_id())
        for i in range(5):
            g1.add_gene([i], P1)
        self.assertTrue(g1.assemble())

        r = random.Random()

        prev_val = g1[0][1]
        some_diff = False
        for i in range(10):
            (g2,) = pyvotune.variators.scramble_mutation(
                r, [g1], {'mutation_rate': 1.0})

            for orig, new in zip(g1, g2):
                if orig != new:
                    some_diff = True

        self.assertTrue(some_diff)
