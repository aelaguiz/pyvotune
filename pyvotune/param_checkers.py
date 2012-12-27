# -*- coding: utf-8 -*-


def noop_checker(val):
    """
    Allows any value to be valid
    """
    return True


def range_checker(val, lower_bound, upper_bound):
    return val >= lower_bound and val < upper_bound


def choice_checker(val, choices):
    return val in choices


def const_checker(val, const_value):
    return val == const_value
