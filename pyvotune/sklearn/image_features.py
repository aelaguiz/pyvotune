# -*- coding: utf-8 -*-

import pyvotune
from sklearn.feature_extraction.image import PatchExtractor


def patchsize_checker(val, min_width, max_width, min_height, max_height):
    width = val[0]
    height = val[1]

    return width >= min_width and width <= max_width and height >= min_height\
        and height <= max_height


def patchsize_generator(rng, min_width, max_width, min_height, max_height):
    return (
        rng.randrange(min_width, max_width + 1), rng.randrange(min_height, max_height + 1))


def get_image_features(n_features, rng):
    pyvotune.dense_input(PatchExtractor)
    pyvotune.non_terminal(PatchExtractor)
    pyvotune.param(
        typename="patchsize",
        checker_fn=patchsize_checker,
        checker_args={
            'min_width': 2,
            'max_width': 200,
            'min_height': 2,
            'max_height': 200
        },
        generator_fn=patchsize_generator,
        generator_args={
            'min_width': 2,
            'max_width': 200,
            'min_height': 2,
            'max_height': 200
        },
        name="patch_size")(PatchExtractor)
    pyvotune.pint(range=(1, 100), name='max_patches', rng=rng)(PatchExtractor)

    return [PatchExtractor]
