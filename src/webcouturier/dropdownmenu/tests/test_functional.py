import unittest2 as unittest
import doctest
from plone.testing import layered

from webcouturier.dropdownmenu.tests.layer import DROPDOWNMENU_FUNCTIONAL


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('browser.txt', ),
                layer=DROPDOWNMENU_FUNCTIONAL),
    ])
    return suite
