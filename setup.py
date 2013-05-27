import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(name='jaspyx',
      version='0.0',
      description='JavaScript expressed in Python',
      classifiers=[
      	  "Programming Language :: Python",
      ],
      author='Ingmar Steen',
      author_email='iksteen@gmail.com',
      url='http://thegraveyard.org/',
      packages=find_packages(),
      scripts=['jaspyxc'],
      include_package_data=True,
      zip_safe=False,
      setup_requires=['nose>=1.0', 'coverage'],
)
