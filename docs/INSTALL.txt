Installation
============

Global python environment
-------------------------

::

 easy_install webcouturier.dropdownmenu
 
Find out how to install setuptools (and EasyInstall) here:
http://peak.telecommunity.com/DevCenter/EasyInstall

Buildout
--------

* Add ``webcouturier.dropdownmenu`` to the list of eggs to install, e.g.
 
  ::
  
     [buildout]
     ...
     eggs =
         ...
         webcouturier.dropdownmenu
        
* Tell the plone.recipe.zope2instance recipe to install a ZCML slug

  ::
  
      [instance]
      recipe = plone.recipe.zope2instance
      ...
      zcml =
          webcouturier.dropdownmenu
        
* Re-run buildout, e.g. with:

  ::
  
      $ ./bin/buildout
          
You can skip the ZCML slug if you are going to explicitly include the package
from another package's configure.zcml file.

Your package's dependency
-------------------------

If you want to automatically install ``webcouturier.dropdownmenu`` when
installing your own package, do the following.

* Add ``webcouturier.dropdownmenu`` as a dependency for your package. Add the
  dependency to your package's **setup.py**'s ``install_requires`` array

  ::
  
      setup(
        ...
        install_requires = [
            ...
            'webcouturier.dropdownmenu',
        ],
        ...
      )

This will automatically download the latest version of the package.

* In your package's **profiles/default/metadata.xml**, within ``<dependencies></dependencies>`` block add

  ::
  
    ...
    <dependency>profile-webcouturier.dropdownmenu:default</dependency>
    ...

* Re-build your buildout and re-start the instance. Now, you should get ``webcouturier.dropdownmenu`` package installed the same very moment you are installing your own package.
