#!/bin/sh

createdb.postgis $1
createlang plpythonu $1
psql -f data_model.sql $1
psql -f extract.sql $1
