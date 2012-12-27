# -*- coding: utf-8 -*-

import unittest
import pyvotune

from pyvotune.pyvotune_globals import *


@pyvotune.empty_input
@pyvotune.sparse_output
@pyvotune.pint(
    range=(0, 5))
@pyvotune.pbool()
class G1:
    def __init__(self, ival, bval):
        self.ival = ival
        self.bval = bval


@pyvotune.sparse_input
@pyvotune.pfloat(range=(-3, 72))
@pyvotune.terminal
class G2:
    def __init__(self, fval):
        self.fval = fval


class TestGenerate(unittest.TestCase):
    def setUp(self):
        pyvotune.set_debug(False)

    def test_term(self):
        @pyvotune.terminal
        class G3:
            def __init__(self):
                pass

        @pyvotune.non_terminal
        class G4:
            def __init__(self):
                pass

        @pyvotune.excl_terminal
        class G5:
            def __init__(self):
                pass

        genome = pyvotune.Genome("terminal_test")
        genome.add_gene([], G3)
        self.assertTrue(genome.validate())

        genome.add_gene([], G4)
        self.assertFalse(genome.validate())

        genome.add_gene([], G3)
        self.assertTrue(genome.validate())

        genome.add_gene([], G5)
        self.assertTrue(genome.validate())

        genome.add_gene([], G3)
        self.assertFalse(genome.validate())

    def test_gen(self):
        gen = pyvotune.Generate(
            gene_pool=[G1, G2],
            max_length=2, noop_frequency=0.)

        for i in range(10):
            genome = gen.generate()

            self.assertTrue(genome)
            self.assertEqual(len(genome), 5)
            self.assertEqual(genome[2][1], G1)
            self.assertEqual(genome[4][1], G2)

        gen = pyvotune.Generate(
            gene_pool=[G1, G2],
            max_length=2, noop_frequency=1.)

        for i in range(10):
            genome2 = gen.generate()
            self.assertFalse(genome2)

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
        @pyvotune.pfloat(range=(-3, 72))
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
