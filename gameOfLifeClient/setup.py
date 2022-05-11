import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='gameOfLifeClient',
      version='0.1',
      description='Client server of the game of life.',
      url='https://github.com/MinaevaKsenia/gameOfLife',
      author='Minaeva Ksenia',
      author_email='minaeva.ksen@gmail.com',
      zip_safe=False,
      long_description=read('README.md'),
      packages=['src', 'src/templates'],
      include_package_data=True
      )
