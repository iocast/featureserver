from unittest import TestSuite

import wfs_base

import ds_spatialite
import ds_postgis
import ds_geoalchemy

def test_suite():
    suite = TestSuite()
    
    suite.addTest(wfs_base.test_suite())
    
    suite.addTests(ds_spatialite.test_suites())
    #suite.addTest(ds_geoalchemy.test_suite())
    
    suite.addTest(ds_postgis.test_suite())
    
    return suite