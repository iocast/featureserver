begin;
delete from history;
delete from object;
delete from txn;
delete from actor;
delete from feature;
select setval('object_id_seq', 1);
insert into actor (email) values ('schuyler@nocat.net');
select create_extract_table('queryable');
select add_extract_column('name', 'queryable', 'title', 'text');
insert into txn (uuid, actor, message) values (
    'cdd83a52f2ac11db921d005056c00008', currval('actor_id_seq'), 'this is a commit msg');
insert into feature (uuid, attrs) values (
    'e9f1acfaf2ac11db921d005056c00008', '(dp1\nS''name''\np2\nS''example object''\np3\ns.');
insert into feature (uuid, attrs) values (
    'fdbc35d4f2ac11db921d005056c00008', '(dp1\nS''name''\np2\nS''example object #2''\np3\ns.');
select currval('object_id_seq');
update feature
    set attrs='(dp1\nS''horse''\np2\nS''yes''\np3\nsS''name''\np4\nS''revised object''\np5\ns.' where id = 2;
select * from history;
select * from feature;
end;
