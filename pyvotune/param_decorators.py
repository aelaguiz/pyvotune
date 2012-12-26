# -*- coding: utf-8 -*-

"""
    pyvotune.param_decorators
    --------------------------

    This module defines decorators which are used to control parameter
    generation and consumption.
"""

from param import Param
from param_checkers import *
from param_generators import *

import random


class param(object):
    """
    General form:
        @pyvotune.param(
            checker_fn=<checker_fn>,
            checker_args=<checker arguments dict>
            generator_fn=<generator_fn>,
            generator_args=<generator arguments dict>,
            rng=random)
    """
    def __init__(
            self, checker_fn, checker_args, generator_fn, generator_args,
            rng=random):
        self.param = Param(
            checker_fn, checker_args, generator_fn, generator_args, rng)

    def __call__(self, cls):
        return add_param(cls, self.param)


class int(param):
    """
    @pyvotune.int(range=(0, 5))
    @pyvotune.int(range=(0, 5), choices=[-2, 0, 7, 10]), rng=random
    """
    def __init__(
            self, range, choices=None, rng=random):

        checker_args = {
            'lower_bound': range[0],
            'upper_bound': range[1]
        }

        generator_fn = range_generator
        generator_args = checker_args

        if choices:
            generator_fn = choice_generator
            generator_args = {
                'choices': choices
            }

        super(int, self).__init__(
            range_checker, checker_args, generator_fn, generator_args,
            rng)


class float(param):
    """
    @pyvotune.float(range=(0, 5.))
    @pyvotune.float(range=(0, 5.), rng=random
    """
    def __init__(
            self, range, rng=random):

        checker_args = {
            'lower_bound': range[0],
            'upper_bound': range[1]
        }

        generator_fn = uniform_generator
        generator_args = checker_args

        super(float, self).__init__(
            range_checker, checker_args, generator_fn, generator_args,
            rng)


class bool(param):
    """
    @pyvotune.bool()
    @pyvotune.bool(rng=random)
    """
    def __init__(
            self, rng=random):

        super(bool, self).__init__(
            nop_checker, None, bool_generator, None,
            rng)


def add_param(cls, param):
    if not hasattr(cls, '_pyvotune_params'):
        cls._pyvotune_params = []

    cls._pyvotune_params.append(param)

    return cls
