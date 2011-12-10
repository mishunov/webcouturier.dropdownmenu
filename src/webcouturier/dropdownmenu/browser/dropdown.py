from Acquisition import aq_inner
from zope.component import getMultiAdapter
from zope.interface import implements

from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.navigation.root import getNavigationRoot

from Products.CMFPlone.browser.navtree import NavtreeQueryBuilder

from plone.app.portlets.portlets.navigation import Assignment

from plone.app.layout.viewlets import common

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

#
# Import ram.cache feature and xhmtl_compression (removes whitespace and so on)
#
from plone.memoize.ram import cache
from plone.memoize.compress import xhtml_compress

from webcouturier.dropdownmenu.browser.interfaces import IDropdownMenuViewlet


class DropdownQueryBuilder(NavtreeQueryBuilder):
    """Build a folder tree query suitable for a dropdownmenu
    """

    def __init__(self, context):
        NavtreeQueryBuilder.__init__(self, context)
        dropdown_properties = getToolByName(
            context, 'portal_properties').dropdown_properties
        dropdown_depth = dropdown_properties.getProperty('dropdown_depth', 3)
        self.query['path'] = {'query': '/'.join(context.getPhysicalPath()),
                              'navtree_start': 1,
                              'depth': dropdown_depth}


class DropdownMenuViewlet(common.GlobalSectionsViewlet):
    """A custom version of the global navigation class that has to have
       dropdown menus for global navigation tabs objects
    """
    implements(IDropdownMenuViewlet)

    #
    # Define a cache key: every instance (probabily only one per site,
    # language and user gets its/his own cache so we don't get the
    # menu retrieved in the wrong language nor conflicts due to view
    # permissions. (A manager might be able to view more pages than an
    # anonymous user.)
    #
    def _render_cachekey(fun, self):

        context = aq_inner(self.context)

        anonymous = getToolByName(
            context, 'portal_membership').isAnonymousUser()

        def get_language(context, request):
            portal_state = getMultiAdapter(
                (context, request), name=u'plone_portal_state')
            return portal_state.locale().getLocaleID()

        return ''.join((
            self.selected_portal_tab,
            get_language(context, self.request),
            str(anonymous),
        ))

    # Cache by

    # ---> Viewlet Name -> should be always identical since no one
    #                      will use two drop down menus, won't he?
    # ---> Selected/Higlighted Tab -> solved current problem
    # ---> By language -> expect to be fixed, if we cache by user
    # ---> User Name -> this is the worst part however if there are
    #                   many logged in users

    #
    # Summary: every user and every visited section gets its own
    # instance in the ram.cache.
    #
    # Suggestion: we should improve this in a manner that not every
    # user needs its own set of instances in the cache
    #
    # If we can't solve this issue caching won't make much use but
    # consume lots of ram.
    #
    # :-(

    #
    # Original template goes here
    #
    _template = ViewPageTemplateFile('dropdown_sections.pt')

    #
    # use cache decoration in order to store/retrieve function output
    # to/from cache
    @cache(_render_cachekey)
    def cached_viewlet(self):
        return xhtml_compress(self._template())

    def index(self):
        if self.enable_caching:
            return self.cached_viewlet()
        else:
            return self._template()

    recurse = ViewPageTemplateFile('dropdown_recurse.pt')

    def update(self):
        common.ViewletBase.update(self)  # Get portal_state and portal_url
        super(DropdownMenuViewlet, self).update()
        context = aq_inner(self.context)
        portal_props = getToolByName(context, 'portal_properties')
        self.properties = portal_props.navtree_properties
        self.dropdown_properties = portal_props.dropdown_properties
        self.enable_caching = self.dropdown_properties.getProperty(
            'enable_caching', False)
        self.enable_parent_clickable = self.dropdown_properties.getProperty(
            'enable_parent_clickable', True)
        self.navroot_path = getNavigationRoot(context)
        self.data = Assignment(root=self.navroot_path)

    def getTabObject(self, tabUrl='', tabPath=None):
        if tabUrl == self.portal_state.navigation_root_url():
            # We are at the navigation root
            return ''
        if tabPath is None:
            # get path for current tab's object
            try:
                # we are in Plone > 3.0.x
                tabPath = tabUrl.split(self.site_url)[-1]
            except AttributeError:
                # we are in Plone 3.0.x world
                tabPath = tabUrl.split(self.portal_url)[-1]

            if tabPath == '' or '/view' in tabPath:
                # It's either the 'Home' or Image tab. It can't have
                # any dropdown.
                return ''

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
            return ''

        portal = self.portal_state.portal()
        portal_path = '/'.join(portal.getPhysicalPath())
        # Check to see if we are using a navigation root. If we are
        # virtual hosting the navigation root as its own domain,
        # the tabPath is no longer rooted at the main portal.
        if portal_path != self.navroot_path:
            portal = portal.restrictedTraverse(self.navroot_path)
        tabObj = portal.restrictedTraverse(tabPath, None)

        if tabObj is None:
            # just in case we have missed any possible path
            # in conditions above
            return ''

        strategy = getMultiAdapter((tabObj, self.data), INavtreeStrategy)
        queryBuilder = DropdownQueryBuilder(tabObj)
        query = queryBuilder()

        data = buildFolderTree(tabObj, obj=tabObj, query=query,
                               strategy=strategy)

        bottomLevel = self.data.bottomLevel or self.properties.getProperty(
            'bottomLevel', 0)

        return self.recurse(children=data.get('children', []), level=1,
                            bottomLevel=bottomLevel).strip()
