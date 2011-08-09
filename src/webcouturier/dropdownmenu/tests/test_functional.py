import unittest
from Testing import ZopeTestCase as ztc
from webcouturier.dropdownmenu.tests.base import DropdownsFunctionalTestCase



def test_suite():
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            'browser.txt',
            test_class=DropdownsFunctionalTestCase),

        ])
