# -*- coding: utf-8 -*-

import unittest
import pyvotune

from pyvotune.pyvotune_globals import *


@pyvotune.empty_input
@pyvotune.sparse_output
@pyvotune.int(
    range=(0, 5))
@pyvotune.bool()
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
            genome = gen.generate()

            self.assertTrue(genome)
            self.assertEqual(len(genome.genes), 2)
            self.assertEqual(genome.genes[0], G1)
            self.assertEqual(genome.genes[1], G2)

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
            genome = gen.generate()

            self.assertTrue(genome.assemble())

    def test_assembly(self):
        gen = pyvotune.Generate(
            gene_pool=[G1, G2],
            max_length=2, noop_frequency=0.)

        genome = pyvotune.Genome("testid")
        genome.add_gene([2, True], G1)
        genome.add_gene([2.5], G2)

        self.assertTrue(genome.assemble())
        individual = genome.assembled

        self.assertEqual(individual[0].ival, 2)
        self.assertEqual(individual[0].bval, True)
        self.assertEqual(individual[1].fval, 2.5)

    def test_assembly_factory(self):
        def make_g3(fval):
            g = G3()
            g.fval = fval
            return g

        @pyvotune.sparse_input
        @pyvotune.float(range=(-3, 72))
        @pyvotune.factory(make_g3)
        class G3:
            def __init__(self):
                pass

        gen = pyvotune.Generate(
            gene_pool=[G1, G3],
            max_length=2, noop_frequency=0.)

        genome = pyvotune.Genome("testid")
        genome.add_gene([2, True], G1)
        genome.add_gene([2.5], G2)

        self.assertTrue(genome.assemble())
        individual = genome.assembled

        self.assertEqual(individual[0].ival, 2)
        self.assertEqual(individual[0].bval, True)
        self.assertEqual(individual[1].fval, 2.5)
