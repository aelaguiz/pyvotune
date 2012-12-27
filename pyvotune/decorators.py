# -*- coding: utf-8 -*-

import collections


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
    """
    This class has custom input and or output validation functions
    """
    for name, method in cls.__dict__.items():
        if hasattr(method, "_pyvotune_input_fn"):
            add_property(cls, 'input', '_fn', method)
        elif hasattr(method, "_pyvotune_output_fn"):
            add_property(cls, 'output', '_fn', method)

    return cls


class input_type(tune):
    """
    This class consumes input of `typename` type
    """
    def __init__(self, typename):
        self.typename = typename

        super(input_type, self).__init__(
            'input', 'typename', typename)


class output_type(tune):
    """
    This class produces output of `typename` type
    """
    def __init__(self, typename):
        self.typename = typename

        super(output_type, self).__init__(
            'output', 'typename', typename)


def input(fn):
    """
    Decorator labels a function as an input validator function
    """
    fn._pyvotune_input_fn = True
    return fn


def output(fn):
    """
    Decorator labels a function as an output validator function
    """
    fn._pyvotune_output_fn = True
    return fn


def loader(cls):
    """
    This gene is only valid as the first gene in the genome
    """
    return empty_input(cls)


def non_terminal(cls):
    """
    This gene is NOT valid as the last gene in a genome
    """
    return add_property(cls, 'position', 'last', False)


def terminal(cls):
    """
    This gene is valid as the last gene in a genome
    """
    return add_property(cls, 'position', 'last', [True, False])


def excl_terminal(cls):
    """
    This gene is ONLY valid as the last gene in a genome
    """
    return add_property(cls, 'position', 'last', True)


def empty_input(cls):
    """
    This gene is only valid with an empty state
    """
    return add_property(cls, 'input', 'empty', True)


def non_empty_input(cls):
    """
    This gene is only valid with a NON empty assembly state
    """
    return add_property(cls, 'input', 'empty', False)


def dense_input(cls):
    return add_property(cls, 'input', 'sparse', False)


def sparse_input(cls):
    return add_property(cls, 'input', 'sparse', True)


def sparse_output(cls):
    return add_property(cls, 'output', 'sparse', True)


def unique(cls):
    cls = add_property(cls, 'input', 'cls_' + cls.__name__, None)
    return add_property(cls, 'output', 'cls_' + cls.__name__, True)


def add_property(cls, direction, name, value):
    if not hasattr(cls, '_pyvotune'):
        cls._pyvotune = collections.defaultdict(dict)

        # Default genes can be input
        cls._pyvotune['input']['empty'] = [True, False]

        # Ensure that genes have to get their terminal status explicitely set
        cls._pyvotune['position']['last'] = False

    cls._pyvotune[direction][name] = value
    return cls
