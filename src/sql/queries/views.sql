-- view newest version of users gathered
CREATE VIEW newest_users AS
    select distinct on (id) * 
    from twitter_user 
    order by id, version desc;

-- view oldest version of users gathered
CREATE VIEW oldest_users AS
    select distinct on (id) *
    from twitter_user
    order by id, version;

-- view with ids of tweets connected to trzaskowski
CREATE VIEW trzaskowski_tweets AS
    SELECT tweet_id
    FROM hashtag
    WHERE lower(tag) ~* '(ObietniceRafałaiHanki|KoniecUkładuHGW|Trzaskowski*|
        Trzaskoski*|Czaskoski*|Czaskowski*|WygrajmyWybory|
        WszystkoWTwoichRekach|24hDlaWarszawy)'
    UNION
    SELECT tweet_id
    FROM mentions
    WHERE user_id=370112160;

-- view with ids of tweets connected to jaki
CREATE VIEW jaki_tweets AS
    SELECT tweet_id
    FROM hashtag
    WHERE lower(tag) ~* '(Jaki*|WarszawaMo*|BudzimyWarszawe|NoweMetro|
            100imyPodBlokiem|NowyImpuls|36impuls*|DzielnicaPrzysz%o%ci|19dzielnica|
            NieMówcie*|NieMowcie*)'
        and
        lower(tag) !~* '(by%jaktrzaskowski|trzaskowski*|
            morawiecki*|kłamaćjakmorawiecki|jakubiak*)'
    UNION
    SELECT tweet_id
    FROM mentions
    WHERE user_id=101576198;

-- view with unique tweets (latest versions of tweets)
CREATE VIEW newest_tweets AS
    SELECT DISTINCT ON (id) *
    FROM tweet
    ORDER BY id, version DESC;