from setuptools import setup, find_packages
import sys, os

version = '0.4'

setup(name='hand',
      version=version,
      description="Feed generator for screen scrapers",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Topic :: Text Processing :: Markup :: XML"],
      keywords='',
      author="Luiz Irber",
      author_email="luiz.irber@gmail.com",
      url="http://code.google.com/p/hand/",
      license="GPLv3",
      packages=find_packages(exclude=['ez_setup', 'examples']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'BeautifulSoup',
          'mechanize',
      ]
)
