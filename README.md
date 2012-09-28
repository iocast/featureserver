FeatureServer
=============
FeatureServer is an implementation of a RESTful Geographic Feature Service. Using standard HTTP methods, you can fetch a representation of a feature or a collection of features, add new data to the service, or delete data from the service. Use it as an aggregator -- post your GeoRSS feeds to it, and then browse them using WFS. Use it as a translator: use the OGR DataSource to load a shapefile and open it in Google Earth.

DataSource (Storage)
--------------------
* __DBM__ -- The DBM datasource uses anydbm combined with pickle to store features in a file on disk. This works on any platform, and works right out of the box.
* __BerkleyDB__ -- The BerkleyDB datasource is a subclass of the DBM datasource. It uses a BerkleyDB module for storage.
* __PostGIS__ -- The PostGIS datasource implements a direct connection to PostGIS, allowing for full featured editing/updating.
* __WFS__ -- The WFS datasource implements read-only access to WFS servers.
* __OGR__ -- The OGR datasource allows you to take any OGR datasource -- such as a shapefile, PostGIS database, GML file, or other formats supported by OGR -- and use it as a backend for a FeatureServer layer.
* __Flickr__ -- Load images from flickr.
* __OSM__ -- Load streets from OpenStreetMap by area, id, or key/value pair.

Service (Input/Output)
----------------------
* __CSV__
* __GeoJSON__ -- input and output in the emerging GeoJSON specification. FeatureServer supports GeoJSON Points, Lines, and Polygons with Rings, as both input and output.
* __GeoRSS Atom (Simple)__ -- input and output of Points/Lines/Polygons (no rings/holes) in GeoRSS Simple (Atom). This allows one to take any GeoRSS Simple Atom feed and feed it to FeatureServer for storage.
* __GML/WFS__ -- Output-only support of WFS/GML.
* __GPX__ -- for Garmin devices
* __HTML__ -- Output-only support of features as HTML files, powered by Cheetah templates.
* __KML__ -- Input and output of Points, Lines, and Polygons from KML.
* __OSM__ -- Output-only support of features as OpenStreetMap '.osm' files. (These files can be opened using JOSM and posted to the OSM server.)
* __OV2__ -- for TomTom devices
* __Shapefile__ -- as zip
* __SQLite/SpatiaLite__ -- points, polyline (linestring), polygon
* __DXF__ -- points, polyline (linestring), polygon

Setup
-----
FeatureServer can be configured to use one of three different server configurations:
* CGI
* mod_python
* Standalone wsgi HTTP server
* FastCGI


Installation
============


Dependencies
------------
* dxfwrite
* lxml
* pyspatialite
* Cheetah
* simplejson
* psycopg2

Mac OSX Mountain Lion
---------------------
GEOS and PROJ is required. Use the OSX Frameworks from http://www.kyngchaos.com/software/frameworks
