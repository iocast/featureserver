from unittest import TestSuite

import wfs_base

import ds_spatialite, ds_postgis, ds_postgishstore
import ds_geoalchemy

def test_suite():
    suite = TestSuite()
    
    suite.addTest(wfs_base.test_suite())
    
    suite.addTests(ds_spatialite.test_suites())
    suite.addTests(ds_postgis.test_suites())
    suite.addTests(ds_postgishstore.test_suites())
    
    suite.addTest(ds_geoalchemy.test_suite())


    return suite