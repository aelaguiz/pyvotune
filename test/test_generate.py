# -*- coding: utf-8 -*-

import unittest
import pyvotune

from pyvotune.pyvotune_globals import *


@pyvotune.empty_input
@pyvotune.sparse_output
@pyvotune.int(
    range=(0, 5))
@pyvotune.bool
class G1:
    def __init__(self, ival, bval):
        self.ival = ival
        self.bval = bval


@pyvotune.sparse_input
@pyvotune.float(range=(-3, 72))
class G2:
    def __init__(self, fval):
        self.fval = fval


class TestGenerate(unittest.TestCase):
    def setUp(self):
        pyvotune.set_debug(False)

    def test_gen(self):
        gen = pyvotune.Generate(
            gene_pool=[G1, G2],
            max_length=2, noop_frequency=0.)

        for i in range(10):
            genome1 = gen.generate()

            self.assertTrue(genome1)
            self.assertEqual(len(genome1.genes), 2)
            self.assertEqual(genome1.genes[0], G1)
            self.assertEqual(genome1.genes[1], G2)

        gen = pyvotune.Generate(
            gene_pool=[G1, G2],
            max_length=2, noop_frequency=1.)

        for i in range(10):
            genome2 = gen.generate()
            self.assertEqual(len(genome2.genes), 2)
            self.assertEqual(genome2.genes[0], NOOP_GENE)
            self.assertEqual(genome2.genes[1], NOOP_GENE)

    def test_params(self):
        gen = pyvotune.Generate(
            gene_pool=[G1, G2],
            max_length=2, noop_frequency=0.)

        for i in range(10):
            genome1 = gen.generate()

            self.assertTrue(genome1.assemble())
