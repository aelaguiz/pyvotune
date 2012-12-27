#!/usr/bin/env python

import re
from setuptools import setup

from pyvotune import __author__, __email__, __version__

DESCRIPTION = 'Python Evolutionary Parametric Hypertuning'


def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            # TODO support version numbers
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements


def parse_dependency_links(file_name):
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))

    return dependency_links

setup(
    packages=['pyvotune'],
    name='pyvotune',
    url='https://github.com/aelaguiz/pyvotune',
    liense="MIT",
    description=DESCRIPTION,

    version=__version__,
    author=__author__,
    author_email=__email__,

    test_suite="test",
    keywords="machine learning, genetic algorithm, sklearn",
    install_requires=parse_requirements('requirements.txt'),
    dependency_links=parse_dependency_links('requirements.txt')
)
