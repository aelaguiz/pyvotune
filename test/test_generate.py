# -*- coding: utf-8 -*-

import unittest
import pyvotune

from pyvotune.pyvotune_globals import *


class TestGenerate(unittest.TestCase):
    def setUp(self):
        pyvotune.set_debug(False)

    def test_gen(self):
        @pyvotune.empty_input
        @pyvotune.sparse_output
        class G3:
            def __init__(self):
                pass

        @pyvotune.sparse_input
        class G4:
            def __init__(self):
                pass

        gen = pyvotune.Generate(
            gene_pool=[G3, G4],
            max_length=2, noop_frequency=0.)

        for i in range(10):
            genome1 = gen.generate()

            self.assertTrue(genome1)
            self.assertEqual(len(genome1.genes), 2)
            self.assertEqual(genome1.genes[0], G3)
            self.assertEqual(genome1.genes[1], G4)

        gen = pyvotune.Generate(
            gene_pool=[G3, G4],
            max_length=2, noop_frequency=1.)

        for i in range(10):
            genome2 = gen.generate()
            self.assertEqual(len(genome2.genes), 2)
            self.assertEqual(genome2.genes[0], NOOP_GENE)
            self.assertEqual(genome2.genes[1], NOOP_GENE)
