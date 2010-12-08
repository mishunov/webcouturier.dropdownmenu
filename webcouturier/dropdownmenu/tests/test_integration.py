"""This is an integration test. It uses PloneTestCase, but does not
use doctest syntax.

You will find lots of examples of this type of test in CMFPlone/tests, for
example.
"""

import unittest
from webcouturier.dropdownmenu.tests.base import DropdownsTestCase
from webcouturier.dropdownmenu.browser.dropdown import DropdownMenuViewlet

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

        self.setRoles('Manager')

        # dummy structure at first
        root_folders_ids = []
        for i in range(2):
            self.portal.invokeFactory('Folder', 'folder-%s'%i)
            root_folders_ids.append('folder-%s'%i)

        # update the dropdownmenu viewlet
        viewlet = DropdownMenuViewlet(self.portal, self.portal.REQUEST, None, None)
        viewlet.update()

        for folder_id in root_folders_ids:
            self.failUnless(folder_id in [tab['id'] for tab in viewlet.portal_tabs])

        # since we don't have subfolders yet, we should not have dropdowns
        for tab_url in [getattr(self.portal, folder_id).absolute_url() for folder_id in root_folders_ids]:
            self.assertEqual(viewlet.getTabObject(tab_url), '')

        # now we add some subfolders to one of the folders
        folder_with_dd = getattr(self.portal, 'folder-0')
        for i in range(2):
            folder_with_dd.invokeFactory('Folder', 'sub-%s'%i)

        folder_with_dd_url = folder_with_dd.absolute_url()
        self.failIf(viewlet.getTabObject(folder_with_dd_url) == '')
        self.failUnless('<a href="http://nohost/plone/folder-0/sub-0"' in viewlet.getTabObject(folder_with_dd_url))

    def test_dropdowns_depth(self):
        # whether the dropdowns follow the depth setting

        self.setRoles('Manager')

        viewlet = DropdownMenuViewlet(self.portal, self.portal.REQUEST, None, None)
        viewlet.update()

        self.assertEqual(viewlet.dropdown_properties.getProperty('dropdown_depth'), 3)

        # 3 is too deep for the test - let's decrease it to 1
        # to see only 1 more level below top folders' tabs
        dropdown_properties = getToolByName(self.portal, 'portal_properties').dropdown_properties
        dropdown_properties.manage_changeProperties(dropdown_depth=1)
        self.assertEqual(viewlet.dropdown_properties.getProperty('dropdown_depth'), 1)

        # dummy structure at first
        # XXX I bet there should be a better way of adding content recursively,
        # but for test this might be good enough
        root_folders_ids = []
        for i in range(2):
            self.portal.invokeFactory('Folder', 'folder-%s'%i)
            root_folders_ids.append('folder-%s'%i)
            root_folder = getattr(self.portal, 'folder-%s'%i)
            for k in range(2):
                root_folder.invokeFactory('Folder', 'folder-%s-sub-%s' % (i, k))
                first_level = getattr(root_folder, 'folder-%s-sub-%s' % (i, k))
                for m in range(2):
                    first_level.invokeFactory('Folder', 'folder-%s-sub-%s-sub-%s' % (i, k, m))

        # let's play with folder-0
        folder_with_dd = getattr(self.portal, 'folder-0')
        folder_with_dd_url = folder_with_dd.absolute_url()

        # dropdown for folder-0 exists?
        self.failIf(viewlet.getTabObject(folder_with_dd_url) == '')

        # do we have first-level subfolder? We should
        self.failUnless('folder-0-sub-0' in viewlet.getTabObject(folder_with_dd_url))

        # do we have second-level subfolder? We should not
        self.failIf('folder-0-sub-0-sub-0' in viewlet.getTabObject(folder_with_dd_url))

        # now change dropdown_depth to include second-level subfolder in dropdown
        # dropdown_properties.manage_changeProperties(dropdown_depth=2)
        # self.assertEqual(viewlet.dropdown_properties.getProperty('dropdown_depth'), 2)
        # self.failUnless('folder-0-sub-0-sub-0' in viewlet.getTabObject(folder_with_dd_url))


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDropdowns))
    return suite
