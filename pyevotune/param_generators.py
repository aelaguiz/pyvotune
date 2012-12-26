# -*- coding: utf-8 -*-


def range_generator(rng, lower_bound, upper_bound):
    return rng.randrange(lower_bound, upper_bound)


def choice_generator(rng, choices):
    return rng.choice(choices)
