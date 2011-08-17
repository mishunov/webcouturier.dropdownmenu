Dropdown menus for Plone
========================

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

If you are not familiar with managing python packages, please read [Packages,
products and
eggs](http://plone.org/documentation/tutorial/buildout/packages-products-and-eggs)
page of the excellent
[tutorial](http://plone.org/documentation/tutorial/buildout) by Martin Aspeli.

Tips
----

* **While disabling clicking the links with children, I want the links in the
  global navigation bar to be clickable nevertheless.**
  
What you need is to customize the ``browser/dropdown.js`` file like the
following:
  
    jQuery(function ($) {
        $('#portal-globalnav ul .noClick').click(function (e) {
            e.preventDefault();
        });
    });
    
Note that we have added **ul** in the jQuery selector. This will stop
clickability of the links in the dropdowns only, but not the section's link in
the global navigation bar itself.
  

Installation
------------

Simply activate ``Dropdown menus profile`` in *Site Setup/Add-ons*.

Thanks
------

Thanks to Wichert Akkerman [Simplon](http://www.simplon.biz) for the help with original version of the package.

Contacts
--------

[Twitter](http://twitter.com/#!/mishunov) ·
[Google+](https://plus.google.com/102311957553961771735/posts)
