from unittest import TestSuite

import wfs

import ds_geoalchemy

def test_suite():
    suite = TestSuite()
    
    suite.addTest(wfs.test_suite())
    
    #suite.addTest(ds_geoalchemy.test_suite())
    
    return suite