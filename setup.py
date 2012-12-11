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
   extra['data_files']=[('/etc', ['src/FeatureServer/assets/config/featureserver.cfg']),
                        ('~/.featureserver/workspace/', ['src/FeatureServer/assets/config/featureserver.cfg']),
                        ('~/.featureserver/templates/', ['src/FeatureServer/assets/templates/default-withmap.html',
                                                         'src/FeatureServer/assets/templates/default.html',
                                                         'src/FeatureServer/assets/templates/exception_report.html'])]
   sys.argv.remove("--debian")
else:
   extra['data_files']=[('featureserver/config/', ['src/FeatureServer/assets/config/featureserver.cfg', 'src/FeatureServer/assets/config/workspace.db']),
                        ('featureserver/templates/', ['src/FeatureServer/assets/templates/default-withmap.html',
                                                      'src/FeatureServer/assets/templates/default.html',
                                                      'src/FeatureServer/assets/templates/exception_report.html'])]

setup(name='FeatureServer',
      version='1.15.1',
      description='A server for geographic features on the web.',
      long_description=read('doc/Readme.txt'),
      author='FeatureServer (iocast)',
      author_email='featureserver@live.com',
      url="http://featureserver.org/",
      keywords="GIS XML XSLT",
      license="MIT",
      
      packages=find_packages('src', exclude=["doc", "tests"]),
      package_dir = {'':'src'},
      
      include_package_data=True,
      
      scripts=['src/featureserver.cgi',
               'src/featureserver.fcgi',
               'src/featureserver_install_config.py',
               'src/featureserver_http_server.py',
               'src/workspace.cgi',
               'src/workspace.fcgi',
               'src/workspace_http_server.py'],
      
      install_requires=['wsgiref>=0.1.2',
                        'dxfwrite>=1.2.0',
                        'lxml>=2.3.5',
                        'pyspatialite>=3.0.1',
                        'Cheetah>=2.4.4',
                        'simplejson>=2.6.2',
                        'psycopg2>=2.4.5',
                        'GeoAlchemy>=0.7.1',
                        'SQLAlchemy>=0.7.9'],
      
      test_suite = 'tests.run_doc_tests',
      zip_safe = False,
      **extra
)
