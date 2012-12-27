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
   extra['data_files']=[('/etc', ['FeatureServer/assets/config/featureserver.cfg']),
                        ('~/.featureserver/workspace/', ['FeatureServer/assets/config/workspace.db']),
                        ('~/.featureserver/templates/', ['FeatureServer/assets/templates/default-withmap.html',
                                                         'FeatureServer/assets/templates/default.html',
                                                         'FeatureServer/assets/templates/exception_report.html'])]
   sys.argv.remove("--debian")
else:
   extra['data_files']=[('config/', ['FeatureServer/assets/config/featureserver.cfg',
                                                   'FeatureServer/assets/config/workspace.db']),
                        ('templates/', ['FeatureServer/assets/templates/default-withmap.html',
                                                      'FeatureServer/assets/templates/default.html',
                                                      'FeatureServer/assets/templates/exception_report.html'])]

setup(name='FeatureServer',
      version='1.15.1',
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
      
      scripts=['scripts/featureserver.cgi',
               'scripts/featureserver.fcgi',
               'scripts/featureserver_install_config.py',
               'scripts/featureserver_http_server.py',
               'scripts/workspace.cgi',
               'scripts/workspace.fcgi',
               'scripts/workspace_http_server.py'],
      
      install_requires=['wsgiref>=0.1.2',
                        'dxfwrite>=1.2.0',
                        'lxml>=2.3.5',
                        'pyspatialite>=3.0.1',
                        'Cheetah>=2.4.4',
                        'simplejson>=2.6.2',
                        'psycopg2>=2.4.5',
                        'GeoAlchemy>=0.7.1',
                        'SQLAlchemy>=0.7.9',
                        'vectorformats>=0.2'],
      
      test_suite = 'tests.run_doc_tests',
      zip_safe = False,
      **extra
)
