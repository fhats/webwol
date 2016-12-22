#!/usr/bin/env python
from distutils.core import setup

setup(name='webwol',
      version='0.3',
      author="Fred Hatfull",
      author_email="webwol@admiralfred.com",
      license="MIT",
      scripts=['webwol.py'],
      url="https://github.com/fhats/webwol",
      description="Web-based WOL packet generator",
      long_description=open("README.md").read())
