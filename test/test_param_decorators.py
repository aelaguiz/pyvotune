# -*- coding: utf-8 -*-

import unittest
import pyevotune


class TestParamDecorators(unittest.TestCase):
    def test_general(self):
        def checker_fn(val, arg1):
            return arg1

        def generator_fn(rng, arg2):
            return arg2

        @pyevotune.param(
            name="p1",
            checker_fn=checker_fn,
            checker_args={
                'arg1': "someval"
            },
            generator_fn=generator_fn,
            generator_args={
                'arg2': "someval2"
            })
        class T1:
            def __init__(self, p1):
                pass

        self.assertTrue(T1._pyevotune_params)
        self.assertEqual(T1._pyevotune_params[0].name, "p1")
        self.assertEqual(T1._pyevotune_params[0].check(None), "someval")
        self.assertEqual(T1._pyevotune_params[0].generate(), "someval2")

    def test_int(self):
        @pyevotune.int_param(
            name="p1",
            range=(0, 5))
        class T2:
            def __init__(self, p1):
                pass

        self.assertTrue(T2._pyevotune_params[0].check(4))
        self.assertFalse(T2._pyevotune_params[0].check(5))

        for i in range(5):
            self.assertTrue(
                T2._pyevotune_params[0].check(
                    T2._pyevotune_params[0].generate()))

    def test_int_choice(self):
        @pyevotune.int_param(
            name="p1",
            range=(0, 5),
            choices=[0, 1])
        class T2:
            def __init__(self, p1):
                pass

        self.assertTrue(T2._pyevotune_params[0].check(4))
        self.assertFalse(T2._pyevotune_params[0].check(5))

        for i in range(15):
            self.assertTrue(
                T2._pyevotune_params[0].generate() in [0, 1])
