# -*- coding: utf-8 -*-

import unittest
import pyvotune


class TestState(unittest.TestCase):
    def setUp(self):
        pyvotune.set_debug(False)

    def test_state(self):
        state = pyvotune.AssemblyState()

        self.assertTrue(state['empty'])

        state['test'] = 5

        self.assertEqual(state['test'], 5)
        self.assertFalse(state['empty'])

    def test_avail(self):
        @pyvotune.sparse_input
        class G1:
            def __init__(self):
                pass

        state = pyvotune.AssemblyState()
        self.assertFalse(state.is_gene_avail(G1))

        state['sparse'] = True
        self.assertTrue(state.is_gene_avail(G1))

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

        state = pyvotune.AssemblyState()
        self.assertFalse(state.is_gene_avail(G2))

        state['avail'] = True
        self.assertTrue(state.is_gene_avail(G2))

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

        state = pyvotune.AssemblyState()
        self.assertTrue(state.is_gene_avail(G3))
        state['test'] = 3
        self.assertFalse(state.is_gene_avail(G3))

        self.assertFalse(state.is_gene_avail(G4))

        state = pyvotune.AssemblyState()

        self.assertTrue(state.is_gene_avail(G3))

        state.gene_update(G3)

        self.assertFalse(state['empty'])
        self.assertTrue(state['sparse'])

        self.assertTrue(state.is_gene_avail(G4))
