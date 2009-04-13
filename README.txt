Overview
--------
You will get the dropdown menus for those items in global navigation that have
the subitems. Submenus are build based on the same policy as the Site Map, so
it will show the same tree as you would get in the Site Map or navigation
portlet being in appropriate section. Requires plone.browserlayer to be
installed in your site.

How it works
------------

Dropdown menus are build based on the same policy as the Site Map, so it will
show the same tree as you would get in the Site Map or navigation portlet
being in appropriate section. This means - no **private** objects for
anonymouses; no objects, excluded from the navigation - exactly the same
behavior you would expect from Site Map or navigation portlet.

How to get it
-------------

- either get the python package from this page and do manual work

- or just add webcouturier.dropdownmenu to your buildout and that's it.
  buildout will get it for you from PyPi.

If you are not familiar with managing python packages, please read `Packages,
products and eggs`_ page of the great tutorial_ by Martin Aspeli who is much
more clever than me and don't spam my inbox ;)

.. _Packages, products and eggs: http://plone.org/documentation/tutorial/buildout/packages-products-and-eggs
.. _tutorial: http://plone.org/documentation/tutorial/buildout


Requirements
------------

webcouturier.dropdownmenu requires plone.browserlayer_ package to be
installed in your site. plone.browserlayer package is shipped with Plone >=
3.1 and thus you don't need anything extra when you have that version of
Plone.

But for Plone 3.0.x < 3.1 the process looks like this:

- if you are creating a new Plone site and want it to support dropdown menus,
  just select 2 extension profiles ``Local browser layer support`` and
  ``Dropdown menus profile`` in **Extension Profiles** select when adding a
  new Plone site;

- if you want to add dropdown menus functionality to already-existing Plone
  site, you need to apply ``Local browser layer support`` extension profile
  and then ``Dropdown menus profile``. You can do it either in
  **portal_setup/Import** or in portal_quickinstaller by simple installation
  procedure.

In Plone 3.1 you can simply install ``Dropdown menus profile`` in
portal_quickinstaller without need of prior installation of ``Local browser
layer support`` (that is not available for installation anyway, since is a
part of core system).

**IMPORTANT** For Plone 3.0.x you should use plone.browserlayer 1.0.rc3. Be
sure to define the right version of plone.browserlayer in your buildout.cfg
(you are using buildout, aren't you? ;)). For Plone 3.1.x just use the version
you have.

.. _plone.browserlayer: http://pypi.python.org/pypi/plone.browserlayer/1.0b3


Copyright and credits
---------------------

`Web Couturier`_   
Thanks to Wichert Akkerman (`Simplon`_) for help   


Author
------

Denys Mishunov

.. _Web Couturier: http://www.webcouturier.com/
.. _Simplon: http://www.simplon.biz