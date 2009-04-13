from zope.component import getUtility
from Products.CMFCore.interfaces import IPropertiesTool


def getDropdownDepth():
    ptool = getUtility(IPropertiesTool)
    return ptool.dropdown_properties.getProperty('dropdown_depth')
    
def cachingEnabled():
    ptool = getUtility(IPropertiesTool)
    return ptool.enable_caching.getProperty('enable_caching')    
