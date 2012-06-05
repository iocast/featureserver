-- View: osm_bus_stops

-- DROP VIEW osm_bus_stops;

CREATE OR REPLACE VIEW osm_bus_stops AS 
 SELECT p.osm_id, p.name, p.operator, p.way
   FROM planet_osm_point p
  WHERE p.highway = 'bus_stop';

ALTER TABLE osm_bus_stops OWNER TO postgres;
GRANT ALL ON TABLE osm_bus_stops TO postgres;
GRANT SELECT ON TABLE osm_bus_stops TO public;
GRANT SELECT, UPDATE, INSERT, DELETE ON TABLE osm_bus_stops TO gisuser;

-- View: osm_restaurants

-- DROP VIEW osm_restaurants;

CREATE OR REPLACE VIEW osm_restaurants AS 
 SELECT p.osm_id, p.name, p.way
   FROM planet_osm_point p
  WHERE p.amenity = 'restaurant';

ALTER TABLE osm_restaurants OWNER TO postgres;
GRANT ALL ON TABLE osm_restaurants TO postgres;
GRANT SELECT ON TABLE osm_restaurants TO public;
GRANT SELECT, UPDATE, INSERT, DELETE ON TABLE osm_restaurants TO gisuser;
