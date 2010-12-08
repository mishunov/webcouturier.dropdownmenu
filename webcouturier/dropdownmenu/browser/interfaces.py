from zope.interface import Interface
from zope import schema
from zope.i18nmessageid import MessageFactory

from plone.theme.interfaces import IDefaultPloneLayer

_ = MessageFactory('webcouturier.dropdownmenu')


class IDropdownConfiguration(Interface):
    """This interface defines the configlet for dropdown menus."""

    dropdown_depth = schema.Int(
        title=_(u"label_dropdown_depth", default=u'Depth of dropdown menus'),
        description=_(u"help_dropdown_depth",
                      default=u'How many levels to list after the top level.'),
        required=True,
        default=3)

    enable_caching = schema.Bool(
        title=_(u"label_enable_caching", default=u"Enable caching"),
        description=_(
            u"help_enable_caching",
            default=(u"WARNING! This is an experimental feature. "
                     u"This is using RAM to store cached template for "
                     u"dropdown menus. Technically every user and "
                     u"every visited section gets its own instance "
                     u"in the ram.cache. Don't enable this if you don't "
                     u"know what this is about. Disable this option "
                     u"if you get unexpected behavior of your global tabs.")),
        default=False,
        required=False)

    enable_parent_clickable = schema.Bool(
        title=_(u"label_enable_parent_clickable",
                default=u"Enable clicking menu items that have children"),
        description=_(
            u"help_enable_parent_clickable",
            default=(u"With this option enabled, every menu item is "
                     u"clickable. With this option disabled, an item is only "
                     u"clickable when it is not a parent so it has no "
                     u"children.")),
        default=True,
        required=False)


class IDropdownSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IDropdownMenuViewlet(Interface):
    """ Marker interface.
        Implements new functionality to global navigation that lets you to
        have dropdown menus for global navigation tabs. Dropdown menu is
        builded with navigation portlet's policy, so dropdowns contain items
        that are only allowed for navigation portlet. If the item is disabled
        for navigation portlet, it is disabled for dropdown menu automatically
    """

    def getTabObject(tabUrl=''):
        """Get the submenu tree for tab object"""
