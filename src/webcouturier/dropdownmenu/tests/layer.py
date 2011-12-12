from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer

from plone.app.testing import setRoles
from plone.app.testing import login
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import PLONE_FIXTURE
from Products.CMFCore.utils import getToolByName


class DropdownmenuBasicLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import webcouturier.dropdownmenu
        self.loadZCML(package=webcouturier.dropdownmenu)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'webcouturier.dropdownmenu:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        workflowTool = getToolByName(portal, 'portal_workflow')
        workflowTool.setDefaultChain('simple_publication_workflow')

        for i in range(2):
            folder_id = 'folder-%s' % i
            portal.invokeFactory('Folder', folder_id)

        setRoles(portal, TEST_USER_ID, ['Member'])


class DropdownmenuLayer(DropdownmenuBasicLayer):

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'webcouturier.dropdownmenu:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        workflowTool = getToolByName(portal, 'portal_workflow')
        workflowTool.setDefaultChain('one_state_workflow')

        for i in range(2):
            folder_id = 'folder-%s' % i
            portal.invokeFactory('Folder', folder_id)
            getattr(portal, folder_id).reindexObject()

        # now we add some subfolders to one of the folders
        folder_one = getattr(portal, 'folder-0')
        for i in range(2):
            folder_id = 'sub-%s' % i
            folder_one.invokeFactory('Folder', folder_id)
            getattr(folder_one, folder_id).reindexObject()

        # And some sub-sub folders
        subfolder = getattr(folder_one, 'sub-0')
        for i in range(2):
            folder_id = 'sub-sub-%s' % i
            subfolder.invokeFactory('Folder', folder_id)
            getattr(subfolder, folder_id).reindexObject()

        setRoles(portal, TEST_USER_ID, ['Member'])

DROPDOWNMENU_BASIC_LAYER = DropdownmenuBasicLayer()
DROPDOWNMENU_BASIC_INTEGRATION = IntegrationTesting(
    bases=(DROPDOWNMENU_BASIC_LAYER, ),
    name="DropdownmenuBasicLayer:Integration")

DROPDOWNMENU_LAYER = DropdownmenuLayer()
DROPDOWNMENU_INTEGRATION = IntegrationTesting(
    bases=(DROPDOWNMENU_LAYER, ), name="DropdownmenuLayer:Integration")
DROPDOWNMENU_FUNCTIONAL = FunctionalTesting(
    bases=(DROPDOWNMENU_LAYER, ), name="DropdownmenuLayer:Functional")
