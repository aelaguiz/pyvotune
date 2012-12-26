# -*- coding: utf-8 -*-

import unittest
import pyvotune


@pyvotune.tune(direction='output', name='sparse', value=True)
class T1:
    def __init__(self):
        pass

    def test_func(self):
        return 2


@pyvotune.sparse_output
class T2:
    def __init__(self):
        pass


@pyvotune.autotune
class T3:
    def __init__(self):
        pass

    def test_func(self):
        return 1

    @pyvotune.output
    def out_state_checker(self, state):
        pass

    @pyvotune.input
    def in_state_checker(self, state):
        pass


class TestDecorators(unittest.TestCase):
    def test_output(self):
        self.assertTrue(T1._pyvotune['output'])
        self.assertTrue(T1._pyvotune['output']['sparse'])

        self.assertTrue(T2._pyvotune['output'])
        self.assertTrue(T2._pyvotune['output']['sparse'])
        self.assertEqual(T1._pyvotune['output'], T2._pyvotune['output'])

        t1 = T1()
        self.assertEqual(t1.test_func(), 2)

    def test_types(self):
        @pyvotune.input_type("int")
        @pyvotune.output_type("bool")
        class T4:
            def __init__(self):
                pass

        self.assertTrue(T4._pyvotune['output'])
        self.assertEqual(T4._pyvotune['input']['typename'], 'int')
        self.assertEqual(T4._pyvotune['output']['typename'], 'bool')

    def test_function(self):
        self.assertEqual(
            T3._pyvotune['output']['_fn'], T3.out_state_checker.im_func)
        self.assertEqual(
            T3._pyvotune['input']['_fn'], T3.in_state_checker.im_func)

        t3 = T3()
        self.assertEqual(t3.test_func(), 1)
