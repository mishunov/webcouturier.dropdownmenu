from zope.component import getUtility
from Products.CMFCore.interfaces import IPropertiesTool


def getDropdownDepth():
    ptool = getUtility(IPropertiesTool)
    return ptool.dropdown_properties.getProperty('dropdown_depth')


def cachingEnabled():
    ptool = getUtility(IPropertiesTool)
    return ptool.dropdown_properties.getProperty('enable_caching', False)


def parentClickable():
    ptool = getUtility(IPropertiesTool)
    return ptool.dropdown_properties.getProperty('enable_parent_clickable', True)
