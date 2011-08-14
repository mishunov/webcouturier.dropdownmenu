Overview
--------
You will get the dropdown menus for those items in global navigation that have
the subitems. Submenus are built based on the same policy as the Site Map, so
it will show the same tree as you would get in the Site Map or navigation
portlet being in appropriate section.

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
products and eggs`_ page of the excellent tutorial_ by Martin Aspeli.

.. _Packages, products and eggs: http://plone.org/documentation/tutorial/buildout/packages-products-and-eggs
.. _tutorial: http://plone.org/documentation/tutorial/buildout


Installation
------------

Simply activate ``Dropdown menus profile`` in *Site Setup/Add-ons*.


Thanks
------

Thanks to Wichert Akkerman (`Simplon`_) for the help with original version of the package.


Author
------

Denys Mishunov
`Twitter`_ · `Google+`_

.. _Simplon: http://www.simplon.biz
.. _Twiter: http://twitter.com/#!/mishunov
.. _Google+: https://plus.google.com/102311957553961771735/posts