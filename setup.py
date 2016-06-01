"""
json_schema_inferencer: Automatically generates schema given json samples

Note that "python setup.py test" invokes pytest on the package. With appropriately
configured setup.cfg, this will check both xxx_test modules and docstrings.

Copyright 2016, Roman Susi.
Licensed under MIT.
"""
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest  # import here, because outside the required eggs aren't loaded yet
        sys.exit(pytest.main(self.test_args))


version = "0.2b1"

setup(name="json_schema_inferencer",
      version=version,
      description="Automatically generates schema given json samples",
      long_description=open("README.rst").read(),
      classifiers=[  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Development Status :: 4 - Beta',
          'Programming Language :: Python'
      ],
      keywords="json schema inference deduce sample",  # Separate with spaces
      author="Roman Susi",
      author_email="roman.susi@kolumbus.fi",
      url="",
      license="MIT",
      packages=find_packages(exclude=['examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      tests_require=['pytest'],
      cmdclass={'test': PyTest},

      install_requires=['validictory'],
      entry_points={
          'console_scripts':
              ['json_schema_inferencer=json_schema_inferencer:main']
      }
)
