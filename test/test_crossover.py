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

        print parents

        for i in range(1):
            children = pyvotune.variators.n_point_crossover(
                r, parents, {'mutation_rate': 1.0})

            print children
            #new_val = g2[0][1]
            #if new_val != prev_val:
                #some_diff = True
            #self.assertTrue(new_val >= 0 and new_val < 5)

        #self.assertTrue(some_diff)

