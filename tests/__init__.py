from unittest import TestSuite

import test_spatialite


def test_suite():
    suite = TestSuite()
    suite.addTest(test_spatialite.test_suite())
    return suite