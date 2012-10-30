#!/usr/bin/env python

import sys

try:
    from setuptools import setup
except:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

readme = file('doc/Readme.txt','rb').read()

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
   extra['data_files']=[('/etc', ['featureserver.cfg'])]
   sys.argv.remove("--debian")
else:
   extra['data_files']=[('FeatureServer', ['featureserver.cfg'])]

setup(name='FeatureServer',
      version='1.12',
      description='A server for geographic features on the web.',
      long_description=readme,
      author='Iocast',
      author_email='featureserver@me.com',
      url='http://featureserver.org/',
      license="MIT",
      packages=['FeatureServer', 
                'FeatureServer.DataSource', 
                'FeatureServer.Service',
                'vectorformats.Formats',
                'vectorformats',
                'web_request'
                ],
      scripts=['featureserver.cgi', 'featureserver.fcgi',
               'featureserver_install_config.py',
               'featureserver_http_server.py'],
      test_suite = 'tests.run_doc_tests',
      zip_safe = False,
      **extra 
     )
