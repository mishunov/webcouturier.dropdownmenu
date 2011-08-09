import unittest2 as unittest

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser

from webcouturier.dropdownmenu.tests import layer


class Helper(unittest.TestCase):

    @property
    def portal(self):
        return self.layer['portal']

    def setRoles(self, roles):
        setRoles(self.portal, TEST_USER_ID, roles)


class DropdownmenuTestCase(Helper):

    layer = layer.DROPDOWNMENU_INTEGRATION


class DropdownmenuFunctionalTestCase(Helper):

    layer = layer.DROPDOWNMENU_FUNCTIONAL

    def getBrowser(self, loggedIn=True):
        """ instantiate and return a testbrowser for convenience """
        browser = Browser(self.layer['app'])
        if loggedIn:
            user = TEST_USER_NAME
            pwd = TEST_USER_PASSWORD
            browser.addHeader('Authorization', 'Basic %s:%s' % (user, pwd))
        return browser
