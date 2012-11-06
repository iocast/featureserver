<pre style="border: 0px; padding: 0px;">
 ___         _                ___                      
| __|__ __ _| |_ _  _ _ _ ___/ __| ___ _ ___ _____ _ _ 
| _/ -_) _` |  _| || | '_/ -_)__ \/ -_) '_\ V / -_) '_|
|_|\___\__,_|\__|\_,_|_| \___|___/\___|_|  \_/\___|_|  
</pre>
<a href="http://featureserver.org" target="_new">FeatureServer</a> is an implementation of a RESTful Geographic Feature Service. Using standard HTTP methods, you can fetch a representation of a feature or a collection of features, add new data to the service, or delete data from the service. Use it as an aggregator -- post your GeoRSS feeds to it, and then browse them using WFS. Use it as a translator: use the OGR DataSource to load a shapefile and open it in Google Earth.

DataSource (Storage)
--------------------
<table>
    <thead>
        <tr>
            <th>Datasource</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>DBM</td>
            <td>The DBM datasource uses anydbm combined with pickle to store features in a file on disk. This works on any platform, and works right out of the box.<br/>The BerkleyDB datasource is a subclass of the DBM datasource. It uses a BerkleyDB module for storage.</td>
        </tr>
        <tr>
            <td>Flickr</td>
            <td>Load images from flickr.</td>
        </tr>
        <tr>
            <td>GeoAlchemy</td>
            <td>GeoAlchemy is an extension of SQLAlchemy, the python database toolkit, for spatial databases. GeoAlchemy datasource for FeatureServer allows you to access features stored in one of the supported spatial databases. As the moment GeoAlchemy supports PostGIS, MySQL and Spatialite.</td>
        </tr>
        <tr>
            <td>OGR</td>
            <td>The OGR datasource allows you to take any OGR datasource -- such as a shapefile, PostGIS database, GML file, or other formats supported by OGR -- and use it as a backend for a FeatureServer layer.</td>
        </tr>
        <tr>
            <td>OSM</td>
            <td>Load streets from OpenStreetMap by area, id, or key/value pair.</td>
        </tr>
        <tr>
            <td>PostGIS</td>
            <td>The PostGIS datasource implements a direct connection to PostGIS, allowing for full featured editing/updating.</td>
        </tr>
        <tr>
            <td>SpatialLite</td>
            <td>SpatiaLite is an open source library intended to extend the SQLite core to support fully fledged Spatial SQL capabilities.</td>
        </tr>
        <tr>
            <td>SQLite</td>
            <td>A simple SQLite datasource that can be used on any website with Python support for SQLite. Creates 2 tables for each layer: one for the features, and one for any attributes/properties pertaining to those features.</td>
        </tr>
        <tr>
            <td>Twitter</td>
            <td>Powered by Twittervision, the twitter datasource lets you use twittervision's API to display the current location of a user.</td>
        </tr>
        <tr>
            <td>WFS</td>
            <td>The WFS datasource implements read-only access to WFS servers.</td>
        </tr>
    </tbody>
</table>

Service (Input/Output)
----------------------
<table>
    <thead>
        <tr>
            <th>Service</th><th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>CSV</td><td></td>
        </tr>
        <tr>
            <td>DXF (AutoCAD)</td><td>Compatible with release 11 and 12, points, polyline (linestring), polygon</td>
        </tr>
        <tr>
            <td>GeoJSON</td><td>input and output in the emerging GeoJSON specification. FeatureServer supports GeoJSON Points, Lines, and Polygons with Rings, as both input and output.</td>
        </tr>
        <tr>
            <td>GeoRSS Atom (Simple)</td><td>input and output of Points/Lines/Polygons (no rings/holes) in GeoRSS Simple (Atom). This allows one to take any GeoRSS Simple Atom feed and feed it to FeatureServer for storage.</td>
        </tr>
        <tr>
            <td>GML/WFS</td><td>Output-only support of WFS/GML.</td>
        </tr>
        <tr>
            <td>GPX</td><td>GPX (the GPS Exchange Format) is a light-weight XML data format for the interchange of GPS data (waypoints, routes, and tracks) between applications and Web services on the Internet. E.g. it can be used for Garmin devices.</td>
        </tr>
        <tr>
            <td>HTML</td><td>Output-only support of features as HTML files, powered by Cheetah templates.</td>
        </tr>
        <tr>
            <td>KML</td><td>Input and output of Points, Lines, and Polygons from KML.</td>
        </tr>
        <tr>
            <td>OSM</td><td>Output-only support of features as OpenStreetMap '.osm' files. (These files can be opened using JOSM and posted to the OSM server.)</td>
        </tr>
        <tr>
            <td>OV2</td><td>TomTom Points of Interest Database</td>
        </tr>
        <tr>
            <td>Shapefile</td><td>The Esri shapefile or simply a shapefile is a popular geospatial vector data format for geographic information systems software. It is developed and regulated by Esri as a (mostly) open specification for data interoperability among Esri and other software products.</td>
        </tr>
        <tr>
            <td>SQLite/SpatiaLite</td><td>SpatiaLite is an open source library intended to extend the SQLite core to support fully fledged Spatial SQL capabilities.</td>
        </tr>
    </tbody>
</table>

for more information visit <a href="http://featureserver.org" target="_new">featureserver.org</a>
