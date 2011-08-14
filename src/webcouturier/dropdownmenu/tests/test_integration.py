import unittest2 as unittest
import zope.interface

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plone.app.layout.navigation.interfaces import INavigationRoot

from Products.CMFCore.utils import getToolByName

from webcouturier.dropdownmenu.browser.dropdown import DropdownMenuViewlet
from webcouturier.dropdownmenu.tests.layer import DROPDOWNMENU_INTEGRATION, \
                                           DROPDOWNMENU_BASIC_INTEGRATION


class TestConfiglet(unittest.TestCase):

    layer = DROPDOWNMENU_INTEGRATION

    def setUp(self):
        portal = self.layer['portal']
        propertiesTool = getToolByName(portal, 'portal_properties')
        self.dmprops = propertiesTool['dropdown_properties']

        self.portal = portal
        self.ps = propertiesTool

    def test_control_panel(self):
        cp = getToolByName(self.portal, "portal_controlpanel")
        self.failUnless('DropdownConfiguration' in [a.getAction(self)['id']
                         for a in cp.listActions()])

    def test_property_sheet_availability(self):
        self.failUnless('dropdown_properties' in self.ps.objectIds())

    def test_settings_available(self):
        settings = ['dropdown_depth',
                    'enable_caching',
                    'enable_parent_clickable']
        for setting in settings:
            self.failUnless(self.dmprops.hasProperty(setting))


class TestDropdownmenu(unittest.TestCase):

    layer = DROPDOWNMENU_BASIC_INTEGRATION

    def setUp(self):
        portal = self.layer['portal']
        request = self.layer['request']
        viewlet = DropdownMenuViewlet(portal, request, None, None)
        setRoles(portal, TEST_USER_ID, ['Manager'])

        # we have 2 folders created on the layer right away
        self.root_folders_ids = ['folder-0', 'folder-1']

        # update the dropdownmenu viewlet
        viewlet.update()

        for folder_id in self.root_folders_ids:
            self.failUnless(folder_id in [tab['id'] for tab in
                                          viewlet.portal_tabs])

        setRoles(portal, TEST_USER_ID, ['Member'])
        self.portal = portal
        self.viewlet = viewlet

    def addSubFolders(self):
        # add some subfolders to one of the folders
        rf = getattr(self.portal, 'folder-0')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        for i in range(2):
            rf.invokeFactory('Folder', 'sub-%s' % i)
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        return rf.absolute_url()

    def test_no_subfolders_without_content(self):
        # since we don't have subfolders yet, we should not have dropdowns
        for tab_url in [getattr(self.portal, folder_id).absolute_url()
                        for folder_id in self.root_folders_ids]:
            self.assertEqual(self.viewlet.getTabObject(tab_url), '')

    def test_dropdownmenus_available(self):
        rf_url = self.addSubFolders()
        self.failIf(self.viewlet.getTabObject(rf_url) == '',
                    "We don't have the sub-folders available in the \
                     global navigation")

    def test_subfolders_in_dropdownmenus(self):
        rf_url = self.addSubFolders()
        self.failUnless('<a href="http://nohost/plone/folder-0/sub-0"'
                       in self.viewlet.getTabObject(rf_url),
                       "The sub-folder's URL is not available in the \
                       global navigation")

    def test_leaks_in_dropdownmenus(self):
        rf_url = self.addSubFolders()
        self.failIf('<a href="http://nohost/plone/folder-0"'
                    in self.viewlet.getTabObject(rf_url),
                    "We have the leakage of the top level folders in the \
                    dropdownmenus")


class TestINavigationRootDropdownmenu(unittest.TestCase):
    """ Test that the dropdownmenus play nice with different INavigationRoot.
    """

    layer = DROPDOWNMENU_INTEGRATION

    def setUp(self):
        portal = self.layer['portal']
        request = self.layer['request']
        # we should have 2 folders in the site's root from the layer. Lets
        # mark one of it's sub-folders ('sub-0') as a navigation root
        self.f1 = portal['folder-0']
        zope.interface.alsoProvides(self.f1, INavigationRoot)
        viewlet = DropdownMenuViewlet(portal, request, None, None)
        viewlet.update()

        self.root_folders_ids = ['sub-0', 'sub-1']
        self.subfolders = ['sub-sub-0', 'sub-sub-1']
        self.portal = portal
        self.request = request
        self.viewlet = viewlet
        self.rf_url = self.f1.absolute_url()

    def test_no_root_folder(self):
        self.failIf('<a href="http://nohost/plone/folder-0"'
                    in self.viewlet.getTabObject(self.rf_url),
                    "The root folder itself is in the globalnavigation")

    def test_dropdownmenus_content(self):
        # Tests the tree builder to aply nice with the INavigationRoot
        self.failIf('<a href="http://nohost/plone/folder-1"' in
                     self.viewlet.getTabObject(self.rf_url),
                    "The dropdown menus don't respect the iNavigationRoot.")
