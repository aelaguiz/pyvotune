# -*- coding: utf-8 -*-

import unittest
import pyvotune


class TestParamDecorators(unittest.TestCase):
    def test_general(self):
        def checker_fn(val, arg1):
            return arg1

        def generator_fn(rng, arg2):
            return arg2

        @pyvotune.param(
            typename="custom type",
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

        self.assertTrue(T1._pyvotune_params)
        self.assertEqual(T1._pyvotune_params[0].check(None), "someval")
        self.assertEqual(T1._pyvotune_params[0].generate(), "someval2")

    def test_pint(self):
        @pyvotune.pint(
            range=(0, 5))
        class T2:
            def __init__(self, p1):
                pass

        self.assertTrue(T2._pyvotune_params[0].check(4))
        self.assertFalse(T2._pyvotune_params[0].check(5))

        for i in range(5):
            self.assertTrue(
                T2._pyvotune_params[0].check(
                    T2._pyvotune_params[0].generate()))

    def test_pint_choice(self):
        @pyvotune.pint(
            range=(0, 5),
            choices=[0, 1])
        class T3:
            def __init__(self, p1):
                pass

        self.assertTrue(T3._pyvotune_params[0].check(4))
        self.assertFalse(T3._pyvotune_params[0].check(5))

        for i in range(15):
            self.assertTrue(
                T3._pyvotune_params[0].generate() in [0, 1])

    def test_pbool(self):
        @pyvotune.pbool()
        class T4:
            def __init__(self, p1):
                pass

        self.assertTrue(T4._pyvotune_params[0].check(4))
        self.assertTrue(T4._pyvotune_params[0].check(-50))
        self.assertTrue(T4._pyvotune_params[0].check(True))

        for i in range(5):
            self.assertTrue(
                T4._pyvotune_params[0].check(
                    T4._pyvotune_params[0].generate()))

    def test_pfloat(self):
        @pyvotune.pfloat(
            range=(-23.3, 73.2))
        class T5:
            def __init__(self, p1):
                pass

        self.assertTrue(T5._pyvotune_params[0].check(-23.3))
        self.assertFalse(T5._pyvotune_params[0].check(73.2))

        for i in range(5):
            self.assertTrue(
                T5._pyvotune_params[0].check(
                    T5._pyvotune_params[0].generate()))

    def test_pint_choice(self):
        @pyvotune.choice(
            choices=[0, 1, 3, 10])
        class T6:
            def __init__(self, p1):
                pass

        self.assertTrue(T6._pyvotune_params[0].check(10))
        self.assertFalse(T6._pyvotune_params[0].check(4))

        for i in range(15):
            self.assertTrue(
                T6._pyvotune_params[0].generate() in [0, 1, 3, 10])

    def test_named_params(self):
        @pyvotune.pfloat(range=(-5, 0), name="p2")
        @pyvotune.pint(range=(0, 5), name="p1")
        class T7:
            def __init__(self, p1, p2):
                self.p1 = p1
                self.p2 = p2

        g = pyvotune.Genome("test")
        t7 = g.construct_gene(T7, g.get_gene_params(T7), [-2.3, 3])

        self.assertEqual(t7.p1, -2.3)
        self.assertEqual(t7.p2, 3)
