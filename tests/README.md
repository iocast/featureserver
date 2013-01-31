<!-- https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet -->
# Database #

## PostgreSQL

### Setup
psql -h localhost -U michel -d featureserver -c ""

```sql
CREATE DATABASE featureserver OWNER michel ENCODING 'UTF8';
CREATE EXTENSION hstore;
CREATE EXTENSION postgis;
```
Tables are created and data inserted automatically.


### PostGISHstore
```sql
BEGIN; 

-- PostGIS with hstore
DropGeometryColumn('', 'fs_point_hstore', 'geom');
DROP TABLE fs_point_hstore

CREATE TABLE fs_point_hstore (id SERIAL, kvp HSTORE );
SELECT AddGeometryColumn ('', 'fs_point_hstore', 'geom',4326, 'POINT', 2, false);

INSERT INTO fs_point_hstore ( kvp, geom ) VALUES ( '"name"=>"p1", "description"=>"d1"', ST_GeomFromText('POINT(8.515048 47.461261)', 4326));
INSERT INTO fs_point_hstore ( kvp, geom ) VALUES ( '"name"=>"p2"', ST_GeomFromText('POINT(7.581210 47.379493)', 4326));
INSERT INTO fs_point_hstore ( kvp, geom ) VALUES ( '"name"=>"p3"', ST_GeomFromText('POINT(7.383456 46.983736)', 4326));
INSERT INTO fs_point_hstore ( kvp, geom ) VALUES ( '"name"=>"p4", "description"=>"d4"', ST_GeomFromText('POINT(7.877841 46.384567)', 4326));
INSERT INTO fs_point_hstore ( kvp, geom ) VALUES ( '"name"=>"p5", "description"=>"d5"', ST_GeomFromText('POINT(8.811679 46.788513)', 4326));
INSERT INTO fs_point_hstore ( kvp, geom ) VALUES ( '"name"=>"p6"', ST_GeomFromText('POINT(8.157992 47.081082)', 4326));

COMMIT;
```
