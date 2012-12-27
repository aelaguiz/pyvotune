# -*- coding: utf-8 -*-


class Param:
    def __init__(
        self, typename, checker_fn, checker_args, generator_fn,
            generator_args, rng, name):
        self.checker_fn = checker_fn
        self.checker_args = checker_args
        self.generator_fn = generator_fn
        self.generator_args = generator_args
        self.rng = rng
        self.typename = typename
        self.name = name

    def __repr__(self):
        if self.name:
            return "%s: %s" % (self.name, self.typename)
        else:
            return self.typename

    def generate(self):
        """
        Parameter generator creates a new parameter of this type
        """
        if self.generator_args:
            return self.generator_fn(self.rng, **self.generator_args)

        return self.generator_fn(self.rng)

    def check(self, val):
        if self.checker_args:
            return self.checker_fn(val, **self.checker_args)

        return self.checker_fn(val)
