CREATE VIEW view1 AS
    select distinct on (id) * 
    from twitter_user 
    order by id, version desc;


\copy (select * from view1) TO '/home/miko/msc/trollemagisterka/src/data/users.csv'  With CSV DELIMITER ',' HEADER;

DROP VIEW view1;