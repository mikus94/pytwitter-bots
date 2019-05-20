-- # most hashtags
select lower(tag) as lt, count(lower(tag)) as clt
from hashtag
group by lt
order by clt desc;

-- # most medias
select link, type, count(link)
from media
group by link, type
order by count(link) desc;

-- # most links
select link, count(link)
from urls
group by link
order by count(link) desc;

-- # most mentions
select m.user_id, tu.screen_name, count(m.user_id) as cid
from mentions as m, newest_users as tu
where m.user_id=tu.id
group by m.user_id, tu.screen_name
order by cid desc;

-- # origin of accounts
select lower(location) as lt, count(lower(location)) as cl
from (
      select distinct on (id) *
      from twitter_user_dsc
      order by id, version desc
  ) as E
group by lt
order by cl desc;

-- # origin of tweets
select lower(place) as lp, count(lower(place)) as clp
from (
      select distinct on (id) *
      from tweet
      order by id, version desc
  ) as E
group by lp
order by clp desc;

-- # mentions
SELECT
        screen_name, count
    FROM
        newest_users as U,
        (
            SELECT user_id, count( *) as count
            FROM mentions
            GROUP BY user_id
        ) as T
    WHERE T.user_id = U.id
    ORDER BY T.count DESC;