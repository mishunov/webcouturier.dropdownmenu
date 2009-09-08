"""This is an integration test. It uses PloneTestCase, but does not
use doctest syntax.

You will find lots of examples of this type of test in CMFPlone/tests, for 
example.
"""

import unittest
from webcouturier.dropdownmenu.tests.base import DropdownsTestCase

from Products.CMFCore.utils import getToolByName

class TestDropdowns(DropdownsTestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """

    def test_property_sheet_availability(self):
        ps = getattr(self.portal, 'portal_properties')
        self.failUnless('dropdown_properties' in ps.objectIds())
        
    def test_dropdown_depth_prop(self):
        ps = self.portal.portal_properties.dropdown_properties
        self.failUnless(ps.hasProperty('dropdown_depth'))
        
    def test_caching_prop(self):
        ps = self.portal.portal_properties.dropdown_properties
        self.failUnless(ps.hasProperty('enable_caching'))        
        
    def test_control_panel(self):
        cp = getToolByName(self.portal, "portal_controlpanel")
        self.failUnless('DropdownConfiguration' in [a.getAction(self)['id']
                         for a in cp.listActions()])
                         
    def test_dropdowns_availability(self):
        # whether we get dropdownmenu at all
        pass
        
    def test_dropdowns_depth(self):
        # whether the dropdowns follow the depth settng
        pass
    
    def test_private_in_dropdown(self):
        # we need to assure that dropdowns follow standard security policy
        pass
    
    def test_dropdowns_for_home(self):
        # we need to be sure dropdowns don't show for 'home' tab
        pass
        
    def test_nav_root(self):
        # If there are language folders at the top of hierarchy we need to be
        # sure that dropdowns start from the language folder's root inside that
        # folder and not from the site's root.
        pass
        
    # Keep adding methods here, or break it into multiple classes or
    # multiple files as appropriate. Having tests in multiple files makes
    # it possible to run tests from just one package:
    #
    #   ./bin/instance test -s example.tests -t test_integration_unit


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDropdowns))
    return suite