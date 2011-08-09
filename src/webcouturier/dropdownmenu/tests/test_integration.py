import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from webcouturier.dropdownmenu.browser.dropdown import DropdownMenuViewlet
from webcouturier.dropdownmenu.tests.base import DropdownmenuTestCase

from webcouturier.dropdownmenu.tests.layer import DROPDOWNMENU_INTEGRATION


class TestConfiglet(unittest.TestCase):

    layer = DROPDOWNMENU_INTEGRATION

    def test_property_sheet_availability(self):
        portal = self.layer['portal']

        ps = getToolByName(portal, 'portal_properties')
        self.failUnless('dropdown_properties' in ps.objectIds())
