# -*- coding: utf-8 -*-

"""
    pyvotune.assembly_decorators
    --------------------------

    This module defines decorators which are used to control how a genome
    is assembled into an individual
"""


class factory(object):
    """
        @pyvotune.factory(
            factory_fn=<factory_fn>
            )
    """
    def __init__(
            self, factory_fn):
        self.factory_fn = factory_fn

    def __call__(self, cls):
        return add_assembly_param(cls, "factory_fn", self.factory_fn)


def add_assembly_param(cls, key, value):
    if not hasattr(cls, '_pyvotune_assembly_params'):
        cls._pyvotune_assembly_params = {}

    cls._pyvotune_assembly_params[key] = value

    return cls
