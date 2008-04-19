from zope.component import getMultiAdapter
from zope.interface import implements

from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree

from Products.CMFPlone.browser.navtree import NavtreeQueryBuilder

from plone.app.portlets.portlets.navigation import Assignment

from plone.app.layout.viewlets import common

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from webcouturier.dropdownmenu.browser.interfaces import IDropdownMenuViewlet

class DropdownQueryBuilder(NavtreeQueryBuilder):
    """Build a folder tree query suitable for a dropdownmenu
    """

    def __init__(self, context):
        NavtreeQueryBuilder.__init__(self, context)
        portal_properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')
        dropdownDepth = navtree_properties.getProperty('dropdownDepth', 3)
        self.query['path']['depth'] = dropdownDepth
            
class DropdownMenuViewlet(common.GlobalSectionsViewlet):
    """A custom version of the global navigation class that has to have 
       dropdown menus for global navigation tabs objects
    """
    implements(IDropdownMenuViewlet)
    
    render = ViewPageTemplateFile('dropdown_sections.pt')          
    recurse = ViewPageTemplateFile('dropdown_recurse.pt')
    
    def update(self):
        common.ViewletBase.update(self) # Get portal_state and portal_url
        super(DropdownMenuViewlet, self).update()
        self.properties = getToolByName(self.context, 'portal_properties').navtree_properties
        self.data = Assignment()

    def getTabObject(self, tabUrl='', tabPath=None):
        if tabPath is None:
            # get path for current tab's object
            try:
                # we are in Plone > 3.0.x
                tabPath = tabUrl.split(self.site_url)[-1]
            except AttributeError:
                # we are in Plone 3.0.x world
                tabPath = tabUrl.split(self.portal_url)[-1]

            if tabPath == '' or '/view' in tabPath:
                # It's either the 'Home' or Image tab. It can't have any dropdown            
                return
            
            if tabPath.startswith("/"):
                tabPath = tabPath[1:]
            elif tabPath.endswith('/'):
                # we need a real path, without a slash that might appear 
                # at the end of the path occasionally
                tabPath = str(tabPath.split('/')[0])
            
            if '%20' in tabPath:
                # we have the space in object's ID that has to be 
                # converted to the real spaces
                tabPath = tabPath.replace('%20', ' ').strip()

        if tabPath == '':
            return

        portal = self.portal_state.portal()
        tabObj = portal.restrictedTraverse(tabPath, None)

        if tabObj is None:
            # just in case we have missed any possible path
            # in conditions above
            return

        strategy = getMultiAdapter((tabObj, self.data), INavtreeStrategy)
        # XXX This works around a bug in plone.app.portlets which was
        # fixed in http://dev.plone.org/svn/plone/changeset/18836
        # When a release with that fix is made this workaround can be
        # removed and the plone.app.portlets requirement in setup.py
        # be updated.
        if strategy.rootPath is not None and strategy.rootPath.endswith("/"):
            strategy.rootPath = strategy.rootPath[:-1]

        queryBuilder = DropdownQueryBuilder(tabObj)
        query = queryBuilder()

        data = buildFolderTree(tabObj, obj=tabObj, query=query, strategy=strategy)

        bottomLevel = self.data.bottomLevel or self.properties.getProperty('bottomLevel', 0)

        return self.recurse(children=data.get('children', []), level=1, bottomLevel=bottomLevel).strip()
