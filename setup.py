from setuptools import setup, find_packages

version = "2.2dev"

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
      author='Denys Mishunov',
      author_email='denys.mishunov@gmail.com',
      url='',
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
      [z3c.autoinclude.plugin]
      target = plone
      """
      )
