from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer

class IDropdownSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer bound to a Skin
       Selection in portal_skins.
       If you need to register a viewlet only for the "Everest Poker Theme"
       skin, this is the interface that must be used for the layer attribute
       in everestPokerTheme/browser/configure.zcml.
    """

class IDropdownMenuViewlet(Interface):
    """ Marker interface.
        Implements new functionality to global navigation that lets you to 
        have dropdwon menus for global navigation tabs. Dropdown menu is 
        builded with navigation portlet's policy, so dropdowns contain items
        that are only allowed for navigation portlet. If the item is disabled
        for navigation portlet, it is disabled for dropdown menu automatically
    """
    
    def getTabObject(tabUrl=''):
        """Get the submenu tree for tab object"""