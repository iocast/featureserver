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
<table>
    <tr>
        <th>Service</th><th>Description</th><th>Exception/Error Output</th>
    </tr>
    <tr>
        <td>CSV</td><td></td><td>comming</td>
    </tr>
    <tr>
        <td>GeoJSON</td><td>input and output in the emerging GeoJSON specification. FeatureServer supports GeoJSON Points, Lines, and Polygons with Rings, as both input and output.</td><td>comming</td>
    </tr>
    <tr>
        <td>GeoRSS Atom (Simple)</td><td>input and output of Points/Lines/Polygons (no rings/holes) in GeoRSS Simple (Atom). This allows one to take any GeoRSS Simple Atom feed and feed it to FeatureServer for storage.</td><td>comming</td>
    </tr>
    <tr>
        <td>GML/WFS</td><td>Output-only support of WFS/GML.</td><td>yes</td>
    </tr>
    <tr>
        <td>GPX</td><td>for Garmin devices</td><td>takes default serivce if supported, GML/WFS otherwise</td>
    </tr>
    <tr>
        <td>HTML</td><td>Output-only support of features as HTML files, powered by Cheetah templates.</td><td>comming</td>
    </tr>
    <tr>
        <td>KML</td><td>Input and output of Points, Lines, and Polygons from KML.</td><td></td>
    </tr>
    <tr>
        <td>OSM</td><td>Output-only support of features as OpenStreetMap '.osm' files. (These files can be opened using JOSM and posted to the OSM server.)</td><td>unkown</td>
    </tr>
    <tr>
        <td>OV2</td><td>for TomTom devices</td><td>takes default serivce if supported, GML/WFS otherwise</td>
    </tr>
    <tr>
        <td>Shapefile</td><td>as zip</td><td></td>
    </tr>
    <tr>
        <td>SQLite/SpatiaLite</td><td>points, polyline (linestring), polygon</td><td></td>
    </tr>
    <tr>
        <td>DXF (AutoCAD)</td><td>Compatible with release 11 and 12, points, polyline (linestring), polygon</td><td></td>
    </tr>
</table>

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

Virtual Environment
-------------------
download virtualenv.py the recent version from http://pypi.python.org/pypi/virtualenv

```
curl https://raw.github.com/pypa/virtualenv/master/virtualenv.py -o virtualenv.py
```

To create a new environment with the name ```featureserver``` run:

```
python virtualenv.py featureserver
```

To activate the virtual env call:

```
source featureserver/bin/activate
```

Now you can install the needed dependencies using the command ```pip install``` as follow:

```
pip install lxml
```

Mac OSX Mountain Lion
---------------------
GEOS and PROJ is required. Use the OSX Frameworks from http://www.kyngchaos.com/software/frameworks
