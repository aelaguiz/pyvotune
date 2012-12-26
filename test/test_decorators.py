# -*- coding: utf-8 -*-

import unittest
import pyevotune


@pyevotune.tune(direction='output', name='sparse', value=True)
class T1:
    def __init__(self):
        pass


@pyevotune.sparse_output
class T2:
    def __init__(self):
        pass


@pyevotune.autotune
class T3:
    def __init__(self):
        pass

    @pyevotune.output
    def out_state_checker(self, state):
        pass

    @pyevotune.input
    def in_state_checker(self, state):
        pass


class TestDecorators(unittest.TestCase):
    def test_output(self):
        self.assertTrue(T1._pyevotune['output'])
        self.assertTrue(T1._pyevotune['output']['sparse'])

        self.assertTrue(T2._pyevotune['output'])
        self.assertTrue(T2._pyevotune['output']['sparse'])
        self.assertEqual(T1._pyevotune['output'], T2._pyevotune['output'])

    def test_function(self):
        self.assertEqual(
            T3._pyevotune['output']['_fn'], T3.out_state_checker.im_func)
        self.assertEqual(
            T3._pyevotune['input']['_fn'], T3.in_state_checker.im_func)
