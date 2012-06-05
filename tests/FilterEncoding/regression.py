'''
Created on May 10, 2011

@author: michel
'''

import unittest

class RegressionTest(unittest.TestCase):
    
    def suite(self):
        modules_to_test = ('SpatialOperatorTest')
        alltests = unittest.TestSuite()
        for module in map(__import__, modules_to_test):
            alltests.addTest(unittest.findTestCases(module))
        return alltests
def suite():
    import tests.FilterEncoding.SpatialOperatorTest as module
    suite = unittest.TestLoader().loadTestsFromModule(module)
    return suite

if __name__ == "__main__":
    #unittest.main(defaultTest='suite')
#    regression = RegressionTest()
#    unittest.main(defaultTest='regression.suite')

    import tests.FilterEncoding.LogicalOperatorTest as lo
    s1 = lo.LogicalOperatorTestSuite()
    import tests.FilterEncoding.SpatialOperatorTest as so
    s2 = so.SpatialOperatorTestSuite()
    import tests.FilterEncoding.ComparisionOperatorTest as co
    s3 = co.ComparisonOperatorTestSuite()

    alltests = unittest.TestSuite([s1, s2, s3])
    unittest.TextTestRunner().run(alltests)
    
