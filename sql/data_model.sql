-- * transaction
--    uuid
--    actor
--    change message
--    bbox
--    timestamp

--- ACTOR

create table actor (
    id serial primary key not null,
    email varchar(255) unique not null
);

insert into actor (email) values ('root@localhost'); -- system user

--- TXN

create table txn (
    uuid char(32) primary key not null,
    id    serial unique not null,
    actor integer  references actor (id) not null,
    message text,
    bbox geometry,
    commit_time timestamp not null
);

create index txn_bbox_idx on txn using gist (bbox gist_geometry_ops);

--- OBJECT

create type dict as (
    name      varchar(255),
    value     text
);

create table object (
    uuid  char(32) not null,
    id    serial not null,
    attrs text,
    shape geometry
);

-- FEATURE

create table feature () inherits (object);
create unique index feature_uuid_idx on feature (uuid);
create unique index feature_id_idx on feature (id);
create index feature_shape_idx on feature using gist (shape gist_geometry_ops);

--- HISTORY

create table history (
    txn_id   char(32) references txn (uuid),
    action   char(1) check (action in ('c', 'u', 'd'))
) inherits (object);

create unique index history_uuid_idx on history (uuid);
create unique index history_id_idx on history (id);
create index history_shape_idx on history using gist (shape gist_geometry_ops);

create rule feature_insert as on insert to feature
    do insert into history 
       select new.uuid, currval('object_id_seq'), new.attrs, new.shape,
        (select uuid from txn where id = currval('txn_id_seq') limit 1)
            as txn_id, 'c' as action;
       
create rule feature_update as on update to feature
    do insert into history 
       select old.uuid, old.id, new.attrs, new.shape,
        (select uuid from txn where id = currval('txn_id_seq') limit 1)
            as txn_id, 'u' as action;
    
create rule feature_delete as on delete to feature
    do insert into history 
       select old.uuid, old.id, old.attrs, old.shape,
        (select uuid from txn where id = currval('txn_id_seq') limit 1)
            as txn_id, 'd' as action;

--  * object
--    uuid
--    local_id
--    attr1
--    attr2
--    attr3
--    attr4
--    serialized_data
--    geometry
--  osm_id    | integer  | 
--  name      | text     | 
--  place     | text     | 
--  landuse   | text     | 
--  leisure   | text     | 
--  natural   | text     | 
--  man_made  | text     | 
--  waterway  | text     | 
--  highway   | text     | 
--  foot      | text     | 
--  horse     | text     | 
--  bicycle   | text     | 
--  motorcar  | text     | 
--  residence | text     | 
--  railway   | text     | 
--  amenity   | text     | 
--  tourism   | text     | 
--  learning  | text     | 
--  building  | text     | 
--  bridge    | text     | 
--  layer     | text     | 
--  junction  | text     | 
--  sport     | text     | 
--  route     | text     | 
--  aeroway   | text     | 
--  way       | geometry | not null

-- 
--  * history
--    object, plus txn uuid
--  
--  * actor
--     email
--     other info
