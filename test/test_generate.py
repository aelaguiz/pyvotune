# -*- coding: utf-8 -*-

import unittest
import pyvotune


class TestGenerate(unittest.TestCase):
    def setUp(self):
        pyvotune.set_debug(True)

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

        genome1 = gen.generate()

        self.assertTrue(genome1)
        self.assertEqual(len(genome1.genes), 2)
