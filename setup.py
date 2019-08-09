#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md', 'r') as fd:
    long_description = fd.read()

setup(
    name='core-people',
    version='0.0',
    description='Research CORE ERM - people module',
    author='Ricardo Ribeiro, Hugo Cachitas',
    author_email='ricardojvr@gmail.com, hugo.cachitas@research.fchampalimaud.org',
    url='https://github.com/research-core/core-people',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    license='CC BY-NC 2.0',
)
