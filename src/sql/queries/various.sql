-- most tweets overall per account
SELECT screen_name, count(E.user_id) as cuid
FROM
    (SELECT DISTINCT id, user_id, count(id) AS cid
    FROM tweet
    GROUP BY id, user_id
    ORDER BY cid DESC) as E,
    newest_users
WHERE newest_users.id=E.user_id
GROUP BY E.user_id, screen_name
ORDER BY cuid DESC;



-- Czaskoski
-- number of tweets with his tags
SELECT lower(tag), count(lower(tag)) as ct
FROM hashtag
WHERE lower(tag) ~* '(ObietniceRafałaiHanki|KoniecUkładuHGW|Trzaskowski*|
    Trzaskoski*|Czaskoski*|Czaskowski*|WygrajmyWybory|
    WszystkoWTwoichRekach|24hDlaWarszawy)'
GROUP BY lower(tag)
ORDER BY ct DESC;

-- tweet id
SELECT tweet_id
FROM hashtag
WHERE lower(tag) ~* '(ObietniceRafałaiHanki|KoniecUkładuHGW|Trzaskowski*|
    Trzaskoski*|Czaskoski*|Czaskowski*|WygrajmyWybory|
    WszystkoWTwoichRekach|24hDlaWarszawy)';

-- id = 370112160
SELECT tweet_id
FROM mentions
WHERE user_id=370112160;


-- tweet ids
(SELECT tweet_id
FROM hashtag
WHERE lower(tag) ~* '(ObietniceRafałaiHanki|KoniecUkładuHGW|Trzaskowski*|
    Trzaskoski*|Czaskoski*|Czaskowski*|WygrajmyWybory|
    WszystkoWTwoichRekach|24hDlaWarszawy)'
UNION
SELECT tweet_id
FROM mentions
WHERE user_id=370112160);


-- jaki
-- number of tweets with its tag
SELECT lower(tag), count(lower(tag)) as ct
FROM hashtag
WHERE lower(tag) ~* '(Jaki*|WarszawaMo*|BudzimyWarszawe|NoweMetro|
    100imyPodBlokiem|NowyImpuls|36impuls*|DzielnicaPrzysz%o%ci|19dzielnica|
    NieMówcie*|NieMowcie*)'
    and
    lower(tag) !~* '(by%jaktrzaskowski|trzaskowski*|
    morawiecki*|kłamaćjakmorawiecki|jakubiak*)'
GROUP BY lower(tag)
ORDER BY ct DESC;

-- tweet id
SELECT tweet_id
FROM hashtag
WHERE lower(tag) ~* '(Jaki*|WarszawaMo*|BudzimyWarszawe|NoweMetro|
    100imyPodBlokiem|NowyImpuls|36impuls*|DzielnicaPrzysz%o%ci|19dzielnica|
    NieMówcie*|NieMowcie*)'
    and
    lower(tag) !~* '(by%jaktrzaskowski|trzaskowski*|
    morawiecki*|kłamaćjakmorawiecki|jakubiak*)';

-- id = 101576198
SELECT tweet_id
FROM mentions
WHERE user_id=101576198;


-- tweet ids
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