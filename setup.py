#!/usr/bin/env python

import sys, os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS',
]

# We'd like to let debian install the /etc/featureserver.cfg,
# but put them in featureserver/featureserver.cfg using setuptools
# otherwise. 
extra = { }
if "--debian" in sys.argv:
   extra['data_files']=[('/etc', ['featureserver/assets/config/featureserver.cfg']),
                        ('~/.featureserver/workspace/', ['featureserver/assets/config/workspace.db']),
                        ('~/.featureserver/templates/', [])]
   sys.argv.remove("--debian")
else:
   extra['data_files']=[('config/', ['featureserver/assets/config/featureserver.cfg',
                                                   'featureserver/assets/config/workspace.db']),
                        ('templates/', [])]

setup(name='FeatureServer',
      version='2.0',
      description='A server for geographic features on the web.',
      long_description=read('doc/Readme.txt'),
      author='FeatureServer (iocast)',
      author_email='featureserver@live.com',
      url="http://featureserver.org/",
      keywords="GIS XML XSLT",
      license="MIT",
      
      #packages=find_packages('src', exclude=["doc", "tests"]),
      #package_dir = {'':'src'},
      packages=find_packages(exclude=["doc", "tests"]),
      include_package_data=True,
      
      scripts=['scripts/featureserver_uwsgi.py',
               'scripts/featureserver_standalone.py'],
      
      install_requires=['vectorformats>=0.2',
                        'bottle>=0.11.6'],
      
      requires=['SQLAlchemy>=0.7.9',
                'GeoAlchemy>=0.7.1',
                'psycopg2>=2.4.5',
                'pysqlite>=2.6.3',
                'pyspatialite>=3.0.1'],
      
      test_suite = 'tests.test_suite',
      zip_safe = False,
      **extra
)
