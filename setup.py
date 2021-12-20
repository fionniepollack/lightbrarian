from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(name='lightbrarian',
      version='0.1.0',
      description='A command line application that allows you to use the Google Books API to search for books and construct a reading list.',
      author='Fionnie Pollack',
      author_email='fionniepollack@gmail.com',
      url='https://github.com/fionniepollack/lightbrarian',
      packages=['lightbrarian'],
      python_requires='>=3.8',
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'lightbrarian = lightbrarian.lightbrarian:cli'
          ]
      },
      install_requires=requirements
     )