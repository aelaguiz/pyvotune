# -*- coding: utf-8 -*-


class Param:
    def __init__(
        self, name, ptype, checker_fn, checker_args, generator_fn,
            generator_args):
        self.name = name
        self.ptype = ptype
        self.checker_fn = checker_fn
        self.checker_args = checker_args
        self.generator_fn = generator_fn
        self.generator_args = generator_args

    def check(self, val):
        return self.checker_fn(val, **checker_args)

    def generate(self):
        return self.generator_fn(**generator_args)

