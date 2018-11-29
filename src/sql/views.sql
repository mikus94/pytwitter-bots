CREATE VIEW newest_users AS
    select distinct on (id) * 
    from twitter_user 
    order by id, version desc;