import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='gameOfLifeServer',
      version='0.1',
      description='Server of the game of life.',
      url='https://github.com/MinaevaKsenia/gameOfLife',
      author='Minaeva Ksenia',
      author_email='minaeva.ksen@gmail.com',
      zip_safe=False,
      packages=['src', 'src/utils'],
      long_description=read('README.md'),
      include_package_data=True
      )
