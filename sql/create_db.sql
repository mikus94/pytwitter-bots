CREATE TABLE twitter_user (
    id                              bigint NOT NULL,
    created_at                      timestamp NOT NULL,
    screen_name                     text,
    description                     text,
    status_count                    integer NOT NULL,
    followers_count                 integer NOT NULL,
    friends_count                   integer NOT NULL,
    favourites_count                integer NOT NULL,
    listed_count                    integer NOT NULL,
    geo_enabled                     boolean NOT NULL,
    verified                        boolean NOT NULL,
    protected                       boolean NOT NULL,
    default_profile                 boolean NOT NULL,
    profile_use_background_image    boolean NOT NULL,
    default_profil_image            boolean NOT NULL,
    lang                            char(2),
    location                        text,
    PRIMARY KEY (id)
);


CREATE TABLE tweet (
    id                              bigint NOT NULL,
    created_at                      timestamp NOT NULL,
    tweet                           text,
    retweet_count                   integer NOT NULL,
    favourites_count                integer NOT NULL,
    lang                            char(2),
    user_id                         bigint NOT NULL,
    place                           text,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id)   REFERENCES twitter_user (id)
);

CREATE TABLE hashtag (
    id                              serial NOT NULL,
    tweet_id                        bigint NOT NULL,
    tag                             text NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (tweet_id)  REFERENCES tweet (id)
);

CREATE TABLE mentions (
    id                              serial NOT NULL,
    tweet_id                        bigint NOT NULL,
    user_id                         bigint NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (tweet_id)  REFERENCES tweet (id),
    FOREIGN KEY (user_id)   REFERENCES twitter_user (id)
);

CREATE TABLE media (
    id                              serial NOT NULL,
    tweet_id                        bigint NOT NULL,
    link                            text NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (tweet_id)  REFERENCES tweet (id)
);

CREATE TABLE retweets (
    id                              serial NOT NULL,
    tweet_id                        bigint NOT NULL,
    user_id                         bigint NOT NULL,
    created_at                      timestamp NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (tweet_id)  REFERENCES tweet (id),
    FOREIGN KEY (user_id)   REFERENCES twitter_user (id)
);

CREATE TABLE quotes (
    id                              serial NOT NULL,
    quoted_id                       bigint NOT NULL,
    tweet_id                        bigint NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (quoted_id) REFERENCES tweet (id),
    FOREIGN KEY (tweet_id)  REFERENCES tweet (id)
);