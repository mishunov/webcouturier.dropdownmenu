from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import ploneSite
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import login
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import PLONE_FIXTURE
from Products.CMFCore.utils import getToolByName


class DropdownmenuLayer(PloneSandboxLayer):

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

        # now we add some subfolders to one of the folders
        folder_one = getattr(portal, 'folder-0')
        for i in range(2):
            folder_id = 'sub-%s' % i
            folder_one.invokeFactory('Folder', folder_id)

        # And some sub-sub folders
        subfolder = getattr(folder_one, 'sub-0')
        for i in range(2):
            folder_id = 'sub-sub-%s' % i
            subfolder.invokeFactory('Folder', folder_id)

        setRoles(portal, TEST_USER_ID, ['Member'])


DROPDOWNMENU_LAYER = DropdownmenuLayer()
DROPDOWNMENU_INTEGRATION = IntegrationTesting(
    bases=(DROPDOWNMENU_LAYER, ), name="DropdownmenuLayer:Integration")
DROPDOWNMENU_FUNCTIONAL = FunctionalTesting(
    bases=(DROPDOWNMENU_LAYER, ), name="DropdownmenuLayer:Functional")
