# -*- coding: utf-8 -*-

"""
    pyvotune.param_decorators
    --------------------------

    This module defines decorators which are used to control parameter
    generation and consumption.
"""

from pyvotune.param import Param
from pyvotune.param_checkers import *
from pyvotune.param_generators import *

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


class choice(param):
    """
    @pyvotune.choice(choices=[-2, 0, 7, 10]), rng=random
    """
    def __init__(
            self, choices, rng=random):

        param.__init__(
            self, choice_checker, {
                'choices': set(choices)
            }, choice_generator, {
                'choices': list(choices)
            },
            rng)


class pint(param):
    """
    @pyvotune.pint(range=(0, 5))
    @pyvotune.pint(range=(0, 5), choices=[-2, 0, 7, 10]), rng=random
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

        param.__init__(
            self, range_checker, checker_args, generator_fn, generator_args,
            rng)


class pfloat(param):
    """
    @pyvotune.pfloat(range=(0, 5.))
    @pyvotune.pfloat(range=(0, 5.), rng=random
    """
    def __init__(
            self, range, rng=random):

        checker_args = {
            'lower_bound': range[0],
            'upper_bound': range[1]
        }

        generator_fn = uniform_generator
        generator_args = checker_args

        param.__init__(
            self, range_checker, checker_args, generator_fn, generator_args,
            rng)


class pbool(param):
    """
    @pyvotune.pbool()
    @pyvotune.pbool(rng=random)
    """
    def __init__(
            self, rng=random):

        param.__init__(
            self, noop_checker, None, bool_generator, None, rng)


def add_param(cls, param):
    if not hasattr(cls, '_pyvotune_params'):
        cls._pyvotune_params = []

    cls._pyvotune_params.append(param)

    return cls
