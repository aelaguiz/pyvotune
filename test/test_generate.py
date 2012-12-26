# -*- coding: utf-8 -*-

import unittest
import pyvotune


class TestGenerate(unittest.TestCase):
    def setUp(self):
        pyvotune.set_debug(True)

    def test_avail(self):
        @pyvotune.sparse_input
        class G1:
            def __init__(self):
                pass

        gen = pyvotune.Generate()
        self.assertFalse(gen.is_gene_avail(G1, {}))
        self.assertTrue(gen.is_gene_avail(G1, {'sparse': True, 'empty': False}))

    def test_avail_fn(self):
        @pyvotune.autotune
        class G2:
            def __init__(self):
                pass

            @pyvotune.input
            def check_fn(self, state):
                if 'avail' not in state:
                    return False

                return state['avail']

        gen = pyvotune.Generate()
        self.assertFalse(gen.is_gene_avail(G2, {}))
        self.assertTrue(gen.is_gene_avail(G2, {'avail': True}))

    def test_out(self):
        @pyvotune.empty_input
        @pyvotune.sparse_output
        class G3:
            def __init__(self):
                pass

        @pyvotune.sparse_input
        class G4:
            def __init__(self):
                pass

        gen = pyvotune.Generate()
        self.assertFalse(gen.is_gene_avail(G3, {'empty': False}))
        self.assertTrue(gen.is_gene_avail(G3, {'empty': True}))
        self.assertFalse(gen.is_gene_avail(G4, {}))

        state = {'empty': True}

        self.assertTrue(gen.is_gene_avail(G3, state))

        gen.update_state(G3, state)

        self.assertFalse(state['empty'])
        self.assertTrue(state['sparse'])

        self.assertTrue(gen.is_gene_avail(G4, state))
