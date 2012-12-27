# -*- coding: utf-8 -*-


def uniform_generator(rng, lower_bound, upper_bound):
    return rng.uniform(lower_bound, upper_bound)


def range_generator(rng, lower_bound, upper_bound):
    return rng.randrange(lower_bound, upper_bound)


def choice_generator(rng, choices):
    return rng.choice(choices)


def bool_generator(rng):
    return bool(rng.getrandbits(1))


def const_generator(rng, const_value):
    return const_value
