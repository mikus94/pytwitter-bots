CREATE TABLE twitter_user (
    id                              bigint NOT NULL,
    created_at                      timestamp NOT NULL,
    screen_name                     text,
    description                     text,
    statuses_count                    integer NOT NULL,
    followers_count                 integer NOT NULL,
    friends_count                   integer NOT NULL,
    favourites_count                integer NOT NULL,
    listed_count                    integer NOT NULL,
    geo_enabled                     boolean NOT NULL,
    verified                        boolean NOT NULL,
    protected                       boolean NOT NULL,
    default_profile                 boolean NOT NULL,
    profile_use_background_image    boolean NOT NULL,
    default_profile_image            boolean NOT NULL,
    lang                            varchar(5),
    location                        text,
    PRIMARY KEY (id)
);


CREATE TABLE tweet (
    id                              bigint NOT NULL,
    created_at                      timestamp NOT NULL,
    tweet                           text,
    retweeted                       boolean NOT NULL,
    retweet_count                   integer NOT NULL,
    favourites_count                integer NOT NULL,
    lang                            char(2),
    user_id                         bigint NOT NULL,
    place                           text,
    -- FOREIGN KEY (user_id)   REFERENCES twitter_user (id),
    PRIMARY KEY (id)
);

CREATE TABLE hashtag (
    -- id                              serial NOT NULL,
    tweet_id                        bigint NOT NULL,
    tag                             text NOT NULL,
    -- FOREIGN KEY (tweet_id)  REFERENCES tweet (id),
    PRIMARY KEY (tweet_id, tag)
);

CREATE TABLE mentions (
    -- id                              serial NOT NULL,
    tweet_id                        bigint NOT NULL,
    user_id                         bigint NOT NULL,
    -- FOREIGN KEY (tweet_id)  REFERENCES tweet (id),
    -- FOREIGN KEY (user_id)   REFERENCES twitter_user (id),
    PRIMARY KEY (tweet_id, user_id)
);

CREATE TABLE urls (
    -- id                              serial NOT NULL,
    tweet_id                        bigint NOT NULL,
    link                            text NOT NULL,
    -- FOREIGN KEY (tweet_id)  REFERENCES tweet (id)
    PRIMARY KEY (tweet_id, link)
);

CREATE TABLE media (
    -- id                              serial NOT NULL,
    tweet_id                        bigint NOT NULL,
    type                            text   NOT NULL,
    link                            text   NOT NULL,
    PRIMARY KEY (tweet_id, link)
);

CREATE TABLE retweets (
    -- id tweeta
    id                              bigint NOT NULL,
    -- id retweeted tweet
    tweet_id                        bigint NOT NULL,
    user_id                         bigint NOT NULL,
    created_at                      timestamp NOT NULL,
    -- FOREIGN KEY (tweet_id)  REFERENCES tweet (id),
    -- FOREIGN KEY (user_id)   REFERENCES twitter_user (id),
    PRIMARY KEY (id)
);

CREATE TABLE quotes (
    -- id of tweet
    id                              bigint NOT NULL,
    -- quoted tweet id
    quoted_id                       bigint NOT NULL,
    -- FOREIGN KEY (quoted_id) REFERENCES tweet (id),
    -- FOREIGN KEY (tweet_id)  REFERENCES tweet (id),
    PRIMARY KEY (id)
);