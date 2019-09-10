\copy (select * from newest_users) TO '~/studia/msc/users.csv'  With CSV DELIMITER ',' HEADER;

\copy (select * from varol_user) TO '~/studia/msc/varol_users.csv'  With CSV DELIMITER ',' HEADER;