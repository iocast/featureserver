<!-- https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet -->
# Progress #

| DataSource | <a href="http://featureserver.org/api.html#api-rest-keywords" target="_blank">Keywords</a> | WFS 1.1.0 | WFS 2.0.0 | Comments |
| ---------- | -------- | --------- | --------- | --- |
| SpatiaLite | Done | Done | Done | |
| PostGIS | Done | Done | Done | |
| PostGISHstore | Done | ~ | ~ | |


# Database #

## PostgreSQL

<!--
psql -h localhost -U michel -d featureserver -c ""
-->

```sql
CREATE DATABASE featureserver OWNER michel ENCODING 'UTF8';
CREATE EXTENSION hstore;
CREATE EXTENSION postgis;
```
Tables are created and data inserted automatically.

