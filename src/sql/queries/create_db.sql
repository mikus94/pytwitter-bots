-- In some tables there are added version field that indicates the version of
-- given data. It is necessary because of data changes in time.

-- table of features for E. Ferrara bot detection technique.
-- all the fields are corresponding the once declared in Twitter API
-- https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
CREATE TABLE twitter_user (
    id                              bigint NOT NULL,
    created_at                      timestamp NOT NULL,
    screen_name                     text,
    statuses_count                  integer NOT NULL,
    followers_count                 integer NOT NULL,
    friends_count                   integer NOT NULL,
    favourites_count                 integer NOT NULL,
    listed_count                    integer NOT NULL,
    geo_enabled                     boolean NOT NULL,
    verified                        boolean NOT NULL,
    protected                       boolean NOT NULL,
    default_profile                 boolean NOT NULL,
    profile_use_background_image    boolean NOT NULL,
    default_profile_image           boolean NOT NULL,

    version                         date NOT NULL,
    PRIMARY KEY (id, version)
);

-- table of users gathered by Varol et al. in his article. Users are labeled
-- whether they are bots or humans (1- bot; 0- human).
CREATE TABLE varol_user (
    id                              bigint NOT NULL,
    created_at                      timestamp NOT NULL,
    screen_name                     text,
    statuses_count                  integer NOT NULL,
    followers_count                 integer NOT NULL,
    friends_count                   integer NOT NULL,
    favourites_count                 integer NOT NULL,
    listed_count                    integer NOT NULL,
    geo_enabled                     boolean NOT NULL,
    verified                        boolean NOT NULL,
    protected                       boolean NOT NULL,
    default_profile                 boolean NOT NULL,
    profile_use_background_image    boolean NOT NULL,
    default_profile_image           boolean NOT NULL,

    version                         date NOT NULL,
    -- filed indicating whether user is a bot or not.
    bot                             boolean NOT NULL,
    PRIMARY KEY (id, version)
);

-- table with additional info of user
CREATE TABLE twitter_user_dsc (
    id                              bigint NOT NULL,
    description                     text,
    location                        text,
    lang                            varchar(5),

    version                         date NOT NULL,
    PRIMARY KEY (id, version)
);

-- table storing tweets
-- fields correspond Twitter API
-- https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
CREATE TABLE tweet (
    -- id of tweet
    id                              bigint NOT NULL,
    -- date of posting tweet
    created_at                      timestamp NOT NULL,
    -- text of tweet
    tweet                           text,
    -- if it was retweeted by authenticated user (Twitter API)
    retweeted                       boolean NOT NULL,
    -- # of retweets
    retweet_count                   integer NOT NULL,
    -- # of times that tweet was added to favourites
    favorite_count                integer NOT NULL,
    -- lang of tweet
    lang                            varchar(5),
    -- id of user that posted the tweet
    user_id                         bigint NOT NULL,
    -- geo information of tweet posting
    place                           text,

    version                         date NOT NULL,
    PRIMARY KEY (id, version)
);

-- table storing hashtags in tweets
CREATE TABLE hashtag (
    -- tweet id
    tweet_id                        bigint NOT NULL,
    -- hashtag that appeared in tweet (without #)
    tag                             text NOT NULL,
    PRIMARY KEY (tweet_id, tag)
);

-- table storing mentions in tweets
CREATE TABLE mentions (
    -- tweet id
    tweet_id                        bigint NOT NULL,
    -- user id who was mentioned
    user_id                         bigint NOT NULL,
    PRIMARY KEY (tweet_id, user_id)
);

-- table storing ulrs shared in tweet
CREATE TABLE urls (
    -- tweet id
    tweet_id                        bigint NOT NULL,
    -- link posted in that tweet
    link                            text NOT NULL,
    PRIMARY KEY (tweet_id, link)
);

-- table storing media appearance in tweet (e.g. photo, video)
CREATE TABLE media (
    -- id of tweet posting media
    tweet_id                        bigint NOT NULL,
    -- type of media posted
    type                            text   NOT NULL,
    -- link to the media
    link                            text   NOT NULL,
    PRIMARY KEY (tweet_id, link)
);

-- table storing information of retweets 
CREATE TABLE retweets (
    -- id tweeta
    id                              bigint NOT NULL,
    -- id retweeted tweet
    tweet_id                        bigint NOT NULL,
    -- retweeting user id
    user_id                         bigint NOT NULL,
    -- date of retweet
    created_at                      timestamp NOT NULL,
    PRIMARY KEY (id)
);

-- table storing quotes of given tweet
CREATE TABLE quotes (
    -- id of tweet
    id                              bigint NOT NULL,
    -- quoted tweet id
    quoted_id                       bigint NOT NULL,
    PRIMARY KEY (id)
);