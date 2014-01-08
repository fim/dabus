#!/usr/bin/env python

from distutils.core import setup

execfile('modules/dabus/version.py')

setup(name='dabus',
    version=__version__,
    description='A gentoo build bot',
    author=__maintainer__,
#    author_email='',
    package_dir = {'': 'modules'},
    packages=['dabus'],
    scripts=['dabus']
)
