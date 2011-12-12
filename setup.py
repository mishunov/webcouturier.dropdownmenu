from setuptools import setup, find_packages

version = "2.2"

setup(name='webcouturier.dropdownmenu',
      version=version,
      description="Dropdown menus for global navigation in Plone",
      long_description=open("README.txt").read()+ '\n' +
                       open("docs/INSTALL.txt").read()+ '\n' +
                       open('CHANGES.txt').read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='web couturier dropdown menu navigation',
      author='Denys Mishunov',
      author_email='denys.mishunov@gmail.com',
      url='http://plone.org/products/webcouturier-dropdownmenu',
      license='GPL',
      packages = find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['webcouturier'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.browserlayer',
      ],
      extras_require={
          'test': ['plone.app.testing',
                   'unittest2',
                   ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """
      )
