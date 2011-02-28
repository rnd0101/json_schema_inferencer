from setuptools import setup, find_packages
import sys, os

version = '0.1a'

setup(name='json_schema_inferencer',
      version=version,
      description="Automatically generates schema given json samples.",
      long_description="""\
Automatically generates schema given json samples.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='json schema inference deduce sample',
      author='Roman Susi',
      author_email='roman.susi@kolumbus.fi',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "simplejson",
          "validictory",
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
