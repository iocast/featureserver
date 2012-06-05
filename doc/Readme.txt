====================================
 Getting Started With FeatureServer 
====================================

---------------------------------------
Simple Python geographic feature server
---------------------------------------

:Date:   2008-05-06
:Copyright: 2006-2008 MetaCarta, Inc. 
:Version: 1.12 
:Manual group: GIS Utilities

DESCRIPTION
===========
FeatureServer is a simple Python-based geographic feature server. It allows 
you to store geographic vector features in a number of different backends,
and interact with them -- creating, updating, and deleting -- via a 
REST-based API.

FeatureServer will run under Python CGI, mod_python, or as a standalone server. 

FeatureServer was designed as a companion to OpenLayers, the BSD licensed web
mapping interface. For help with setting up FeatureServer for use with 
OpenLayers, please feel free to stop by #featureserver, on irc.freenode.net, or 
to send email to featureserver@featureserver.org.

FeatureServer is released under a copyright only open source license similar
to the BSD license.

RUNNING UNDER CGI
=================

* Extract the code to some web directory (e.g. in /var/www).
* Edit featureserver.cfg to point the 'file' attribute of the 'scribble'
  datasource to the location you wish to save your database.
* Permit CGI execution in the FeatureServer directory.
  For example, if FeatureServer is to be run with Apache, the
  following must be added in your Apache configuration,   
  where /var/www/featureserver is the directory resulting from
  the code extraction. 
  
  ::

    <Directory /var/www/featureserver>
         AddHandler cgi-script .cgi
         Options +ExecCGI
    </Directory>

* Visit:
  
  http://example.com/yourdir/featureserver.cgi/scribble/all.atom
  
* If you see an empty GeoRSS feed, you have set up your configuration 
  correctly. Congrats!

Python Prerequisites
--------------------
In order to use the default demo included with FeatureServer, you must have
the simplejson module installed. If you do not, you can add it by doing the
following:

  $ wget http://cheeseshop.python.org/packages/source/s/simplejson/simplejson-1.7.1.tar.gz
  $ tar -zvxf simplejson-1.7.1.tar.gz
  $ cp -r simplejson-1.7.1/simplejson /var/www/featureserver

Note that these instructions are for Linux systems: the end goal is to extract
the simplejson directory from the distribution and put it in the root of your
FeatureServer install.

Other dependencies for DataSources and Services are outlined in their 
respective documentation files. 

Non-standard Python Location
----------------------------
If your Python is not at /usr/bin/python on your system, you will need to
change the first line of featureserver.cgi to reference the location of your 
Python binary. A common example is:

  ::

     #!/usr/local/bin/python

Under Apache, you might see an error message like:

  ::

    [Wed Mar 14 19:55:30 2007] [error] [client 127.0.0.1] (2)No such file or 
      directory: exec of '/www/featureserver.cgi' failed

to indicate this problem.

You can typically locate where Python is installed on your system via the
command 'which python'.

Windows users: If you are using Windows, you should change the first line 
of featureserver.cgi to read:

  ::

    #!C:/Python/python.exe -u

C:/Python should match the location Python is installed under on your 
system. In Python 2.5, this location is C:/Python25 by default.  

RUNNING UNDER MOD_PYTHON
========================

* Extract the code to some web directory (e.g. /var/www).
* Edit featureserver.cfg to point the 'file' attribute of the 'scribble'
  datasource to the location you wish to save your database.
* Add the following to your Apache configuration, under a <Directory> heading:
  
  ::
  
      AddHandler python-program .py
      PythonPath sys.path+['/path/to/featureserver/FeatureServer', '/path/to/featureserver']
      PythonHandler FeatureServer.Server
      PythonOption FeatureServerConfig /path/to/featureserver.cfg
  
* An example might look like:

  ::
  
    <Directory /var/www/featureserver/>
        AddHandler python-program .py
        PythonPath sys.path+['/var/www/featureserver/FeatureServer', '/var/www/featureserver']
        PythonHandler FeatureServer.Server 
        PythonOption FeatureServerConfig /var/www/featureserver/featureserver.cfg
    </Directory>
  
* In this example, /var/www/featureserver is the directory resulting from
  the code extraction. 
* Visit the URL described above, replacing featureserver.cgi with 
  featureserver.py
* If you see an empty GeoRSS file you have set up your configuration correctly.
  Congrats!
* Note that mod_python has not yet been well tested, and may not work well
  for all data sources.

 
RUNNING STANDALONE (UNDER WSGI)
===============================

FeatureServer comes with a standalone HTTP server which uses the WSGI handler. 
This implementation depends on *Python Paste*, which can be downloaded from:
  
  http://cheeseshop.python.org/pypi/Paste

For versions of Python earlier than 2.5, you will also need to install 
wsgiref:

  http://cheeseshop.python.org/pypi/wsgiref

Once you have all the prerequisites installed, simply run:

  ::
  
    python featureserver_http_server.py

This will start a webserver listening on port 8080, after which you should
be able to open:

  ::
  
    http://hostname:8080/scribble/all.atom

to see your first file.

RUNNING UNDER FASTCGI
=====================

FeatureServer comes with a fastcgi implementation. In order to use this 
implementation, you will need to install flup, available from:
  
  http://trac.saddi.com/flup

This implementation also depends on Python Paste, which can be downloaded 
from:
  
  http://cheeseshop.python.org/pypi/Paste

Once you have done this, you can configure your fastcgi server to use
featureserver.fcgi.

Configuring FastCGI is beyond the scope of this documentation.

CONFIGURATION
=============
FeatureServer is configured by a config file, defaulting to featureserver.cfg.
FeatureServer data source documentation is available in doc/DataSources.

USING FEATURESERVER WITH OPENLAYERS
===================================

To run OpenLayers with FeatureServer, the URL passed to the 
OpenLayers.Layer.WFS constructor must point to the FeatureServer script, 
i.e. featureserver.cgi or featureserver.py. As an example see the 
index.html file included in the FeatureServer distribution.

Note: index.html assumes FeatureServer is set up under CGI (see above). 
If you set up FeatureServer under mod_python you'd need to slighly 
modify index.html: the URL passed to the OpenLayers.Layer.WFS constructor 
must point to the mod_python script as opposed to the CGI script, so replace 
featureserver.cgi with featureserver.py. Similarly, you would need to edit 
this URL if you were to use FeatureServer with the standalone HTTP Server 
or FastCGI.

SEE ALSO
========

http://featureserver.org/

http://openlayers.org/
