# -*- coding: utf-8 -*-

import collections
from functools import wraps


class tune(object):
    """
    Base tune decorator which allows arguments to configure
    """
    def __init__(self, direction=None, name=None, value=None):
        self.direction = direction
        self.name = name
        self.value = value

    def __call__(self, cls):
        return add_property(cls, self.direction, self.name, self.value)


def autotune(cls):
    for name, method in cls.__dict__.items():
        if hasattr(method, "_pyvotune_input_fn"):
            add_property(cls, 'input', '_fn', method)
        elif hasattr(method, "_pyvotune_output_fn"):
            add_property(cls, 'output', '_fn', method)

    return cls


def input(fn):
    fn._pyvotune_input_fn = True
    return fn


def output(fn):
    fn._pyvotune_output_fn = True
    return fn


def empty_input(cls):
    return add_property(cls, 'input', 'empty', True)


def non_empty_input(cls):
    return add_property(cls, 'input', 'empty', False)


def sparse_input(cls):
    cls = non_empty_input(cls)
    return add_property(cls, 'input', 'sparse', True)


def sparse_output(cls):
    return add_property(cls, 'output', 'sparse', True)


def add_property(cls, direction, name, value):
    if not hasattr(cls, '_pyvotune'):
        cls._pyvotune = collections.defaultdict(dict)

    cls._pyvotune[direction][name] = value
    return cls
