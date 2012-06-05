CREATE TABLE extract (
    id BIGINT REFERENCES feature(id) ON DELETE CASCADE
);

CREATE VIEW extract_keys AS
    SELECT relname AS tabname, attname AS colname, typname AS coltype,
        col_description(pg_class.oid, attnum) AS attrkey
        FROM pg_class, pg_attribute, pg_type
        WHERE attrelid = pg_class.oid
            AND atttypid = pg_type.oid
            AND attnum > 0 
            AND col_description(pg_class.oid, attnum) IS NOT NULL;

CREATE OR REPLACE FUNCTION
    prepare_extract_plans () RETURNS VOID AS '
    plans  = GD["vespucci_plans"] = {}
    tables = {}
    for extract in plpy.execute("SELECT * FROM extract_keys;"):
        tabname = extract["tabname"]
        if not tables.has_key(tabname): tables[tabname] = {}
        tables[tabname][extract["colname"]] = (
                                  extract["attrkey"], extract["coltype"])

    for tabname, table in tables.iteritems():
        plans[tabname] = {}
        columns    = table.keys()
        attrkeys   = [col[0] for col in table.values()]
        coltypes   = [col[1] for col in table.values()] + ["int4"]
        params     = ["$" + str(n) for n in range(1,len(table)+1)]
        predicates = [("%s = %s" % x) for x in zip(columns, params)]
        insert = "INSERT INTO %s (%s, id) VALUES (%s, $%d);" % (
            tabname, ", ".join(columns), ", ".join(params), len(table)+1)
        update = "UPDATE %s SET %s WHERE id = $%d;" % (
            tabname, ", ".join(predicates), len(table)+1)
        plans[tabname]["keys"]   = attrkeys
        plans[tabname]["insert"] = plpy.prepare(insert, coltypes)
        plans[tabname]["update"] = plpy.prepare(update, coltypes)
    return 0
' LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION
    update_extract_tables (varchar, bigint, text) RETURNS VOID AS '

    import cPickle

    if not GD.has_key("vespucci_plans"):
        plpy.execute("SELECT prepare_extract_plans();")
    plans = GD["vespucci_plans"]

    cmd, object_id, blob = args
    attrs = cPickle.loads(blob.decode("string-escape"))

    for tabname, plan in plans.iteritems():
        vals = [attrs.get(key, None) for key in plan["keys"]] + [object_id]
        plpy.execute( plan[cmd], vals )
            
' LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION
    update_extract (varchar, bigint, text) RETURNS VOID AS '

    import cPickle
    if not GD.has_key("vespucci_plans"):
        plpy.execute("SELECT prepare_extract_plans();")
    plans = GD["vespucci_plans"]

    tabname, object_id, blob = args
    attrs = cPickle.loads(blob.decode("string-escape"))

    plan = plans[tabname]
    vals = [attrs.get(key, None) for key in plan["keys"]] + [object_id]
    plpy.execute( plan["update"], vals )
' LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION
    build_extract_table (varchar) RETURNS VOID AS '
    plpy.execute("SELECT update_extract(''%s'', id, attrs) FROM feature;"
                    % args[0])
' LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION
    create_extract_table (varchar) RETURNS VARCHAR AS '
    tabname = args[0]
    plpy.execute( """CREATE TABLE %s () INHERITS (extract);""" % tabname )
    plpy.execute( """CREATE INDEX %s_id_idx ON %s (id);""" % (tabname,tabname))
    plpy.execute( """INSERT INTO %s SELECT id FROM feature;""" % tabname )
    return tabname
' LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION 
    add_extract_column (varchar, varchar, varchar, varchar)
    RETURNS VARCHAR AS '
    tabname, colname, coltype, attrkey = args
    plpy.execute("ALTER TABLE %s ADD COLUMN %s %s;" %
                        (tabname, colname, coltype))
    plpy.execute("COMMENT ON COLUMN %s.%s IS ''%s'';" %
                        (tabname, colname, attrkey.replace("''", "''''")))
    plpy.execute("SELECT prepare_extract_plans();")
    return colname
' LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION 
     drop_extract_column (varchar, varchar) RETURNS VARCHAR AS '
    tabname, colname = args
    plpy.execute("ALTER TABLE %s DROP COLUMN %s;" % (tabname, colname))
    plpy.execute("SELECT prepare_extract_plans();")
    return colname
' LANGUAGE plpythonu;

CREATE RULE feature_insert_extract AS ON INSERT TO feature
  DO SELECT update_extract_tables('insert', currval('object_id_seq'), new.attrs);

CREATE RULE feature_update_extract AS ON UPDATE TO feature
  DO SELECT update_extract_tables('update', old.id, new.attrs);
