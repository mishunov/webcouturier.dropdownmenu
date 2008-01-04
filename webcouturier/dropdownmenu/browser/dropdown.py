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
        portal_url = getToolByName(context, 'portal_url')
        portal_properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')
        dropdownDepth = navtree_properties.getProperty('dropdownDepth', 3)
        self.query['path'] = {'query' : portal_url.getPortalPath(),
                              'depth' : dropdownDepth}
            
class DropdownMenuViewlet(common.GlobalSectionsViewlet):
    """A custom version of the global navigation class that has to have 
       dropdown menus for global navigation tabs objects
    """
    implements(IDropdownMenuViewlet)
    
    render = ViewPageTemplateFile('dropdown_sections.pt')          
    recurse = ViewPageTemplateFile('dropdown_recurse.pt')
    
    def __init__(self, context, request, view, manager):
        common.GlobalSectionsViewlet.__init__(self, context,
                        request, view, manager)
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.portal = self.portal_state.portal()
        self.portal_url = self.portal_state.portal_url()

        self.properties = getToolByName(self.context, 'portal_properties').navtree_properties
        self.data = Assignment()

    def getTabObject(self, tabUrl=''):
        # get path for current tab's object
        tabPath = tabUrl.split(self.portal_url)[-1]

        if tabPath == '':
            # It's the 'Home' tab. It can't have any dropdown            
            return
        elif tabPath[0] == '/':
               tabPath = tabPath[1:]
        elif tabPath.split('/'):
            # we need a real path, without a slash that might appear 
            # occasionally
            tabPath = str(tabPath.split('/')[0])

        if tabPath != '':
            tabObj = self.portal.restrictedTraverse(tabPath, None) 
 
            strategy = getMultiAdapter((tabObj, self.data), INavtreeStrategy)         
            
            queryBuilder = DropdownQueryBuilder(tabObj)
            query = queryBuilder()

            data = buildFolderTree(tabObj, obj=tabObj, query=query, strategy=strategy)
            
            bottomLevel = self.data.bottomLevel or self.properties.getProperty('bottomLevel', 0)

            return self.recurse(children=data.get('children', []), level=1, bottomLevel=bottomLevel).strip()
