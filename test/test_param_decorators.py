# -*- coding: utf-8 -*-

import unittest
import pyevotune


class TestParamDecorators(unittest.TestCase):
    def test_general(self):
        #@pyevotune.param(
            #name=<name>,
            #checker_fn=<checker_fn>,
            #checker_args=<checker arguments dict>
            #generator_fn=<generator_fn>,
            #generator_args=<generator arguments dict>)

        def checker_fn(val, arg1):
            print "checker_fn called"

        def generator_fn(arg2):
            print "generator_fn called"

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
