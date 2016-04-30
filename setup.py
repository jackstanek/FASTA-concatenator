#!/usr/bin/env python3

from distutils.core import setup

setup(name='fastacat',
      version='0.0.3',
      description='Concatenates FASTA genetic data between exons',
      author='Jack Stanek',
      author_email='stane064@umn.edu',
      url='https://github.com/jackstanek/FASTA-concatenator',
      packages=['fastacat'],
      scripts=['fastacat/cli/fastacat'])
