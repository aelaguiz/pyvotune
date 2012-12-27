# -*- coding: utf-8 -*-

import unittest
import pyvotune
import random

from pyvotune.util.id_generator import get_id


class TestCrossover(unittest.TestCase):
    def setUp(self):
        pyvotune.set_debug(False)

    def test_n_point(self):
        @pyvotune.pint(
            range=(0, 5))
        class P1:
            def __init__(self, intparam):
                self.intparam = intparam

        g1 = pyvotune.Genome(get_id())
        g1.add_gene([0], P1)
        g1.add_gene([0], P1)
        self.assertTrue(g1.assemble())

        g2 = pyvotune.Genome(get_id())
        g2.add_gene([1], P1)
        g2.add_gene([1], P1)
        self.assertTrue(g2.assemble())

        r = random.Random()

        prev_val = g1[0][1]
        some_diff = False

        parents = [g1, g2]

        for i in range(1):
            children = pyvotune.variators.n_point_crossover(
                r, parents, {})

            self.assertTrue(children)

            for child in children:
                for parent in parents:
                    found_diff = False
                    for c, p in zip(child, parent):
                        if c != p:
                            found_diff = True

                    self.assertTrue(found_diff)

    def test_uniform(self):
        @pyvotune.pint(
            range=(0, 5))
        class P1:
            def __init__(self, intparam):
                self.intparam = intparam

        g1 = pyvotune.Genome(get_id())
        g1.add_gene([0], P1)
        g1.add_gene([0], P1)
        self.assertTrue(g1.assemble())

        g2 = pyvotune.Genome(get_id())
        g2.add_gene([1], P1)
        g2.add_gene([1], P1)
        self.assertTrue(g2.assemble())

        r = random.Random()

        prev_val = g1[0][1]
        some_diff = False

        parents = [g1, g2]

        for i in range(1):
            children = pyvotune.variators.uniform_crossover(
                r, parents, {'ux_bias': 1.0})

            self.assertTrue(children)

            found_diff = False

            for child in children:
                for parent in parents:
                    for c, p in zip(child, parent):
                        if c != p:
                            found_diff = True

            self.assertTrue(found_diff)
