# -*- coding: utf-8 -*-


class Param:
    def __init__(
        self, name, checker_fn, checker_args, generator_fn,
            generator_args, rng):
        self.name = name
        self.checker_fn = checker_fn
        self.checker_args = checker_args
        self.generator_fn = generator_fn
        self.generator_args = generator_args
        self.rng = rng

    def check(self, val):
        return self.checker_fn(val, **self.checker_args)

    def generate(self):
        return self.generator_fn(self.rng, **self.generator_args)

