#!/usr/bin/env python

from distutils.core import setup

setup(name='Pluton',
      version='1.0',
      description='Pluton Crypto Analysis and Trading Bot',
      author='David Lyon',
      author_email='david.lyon@clixx.io',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=['pandas', 'matplotlib','cryptocmd','cheetah','pytable','appdirs','configparser'],
      scripts=['src/pluton'],
     )
     
