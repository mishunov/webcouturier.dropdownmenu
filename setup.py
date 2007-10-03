from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='webcouturier.dropdownmenu',
      version=version,
      description="Dropdown menus for global navigation in Plone",
      long_description=open("README.txt").read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='web couturier dropdown menu navigation',
      author='Denis Mishunov (Web Couturier)',
      author_email='denis@webcouturier.com',
      url='http://svn.plone.org/svn/collective/webcouturier.dropdownmenu',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['webcouturier'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.browserlayer',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
