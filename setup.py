#!/usr/bin/env python
from distutils.core import setup

setup(name='webwol',
      version='1.0-dev',
      author="Fred Hatfull",
      author_email="webwol@admiralfred.com",
      license="MIT",
      scripts=['webwol.py'],
      url="https://github.com/fhats/webwol",
      description="Web-based WOL packet generator",
      long_description=open("README.md").read())
