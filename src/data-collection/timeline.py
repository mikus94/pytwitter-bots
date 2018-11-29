# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
Application downloading tweets using Twitter API.
"""
"""
Downloading module.
"""
import tweepy
from time import sleep


from .storage.db import DbHandler
from .storage.files import FileHandler
from .storage.logger import Logger

from .configs import config


# create authentication objects
auth = tweepy.OAuthHandler(config.cost_key, config.cost_skey)
auth.set_access_token(config.acc_key, config.acc_skey)

# create API
api = tweepy.API(
    auth,
    wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True,
    retry_count=10,
    retry_delay=5
)


db = DbHandler()
storage = FileHandler("timeline")
logger = Logger("timeline")

# get all users ids
# get only these users that are not verified
# only they can be bots and may be needed to analyze their tweets.
select_newest_users_sql = (
    """
    SELECT DISTINCT ON (id) id, screen_name
    FROM twitter_user
    WHERE verified=false
    ORDER BY id, version DESC;
    """
)

users = db.execute_select(select_newest_users_sql)

for user in users:
    # log user info
    logger.print_nnl("\n")
    logger.print_nnl("Start processing: {}\nid: {}".format(user[1], user[0]))
    # opts
    count = 100
    search_opts = {
        'user_id': user[0],
        'count': 100
    }
    last_id=0
    backoff_counter = 1
    while True:
        try:
            for tweet in api.user_timeline(**search_opts):

                # get tweet data
                tweet_json = tweet._json
                user_id = tweet_json['user']['id_str']
                last_id = tweet_json['id']
                # store data
                storage.save_user_tweet(user_id, tweet_json)
                count -= 1
                
            last_id=0
            break
        except tweepy.RateLimitError as e:
            logger.print_nnl("ERROR!")
            logger.print_nnl("During processing \'" + user[1] + "\'.")
            logger.print_nnl("Tweet id was: \'" + str(last_id) + "\'.")
            logger.print_nnl(str(e))

            search_opts['max_id'] = int(last_id)
            search_opts['count'] = count

            sleep(60*backoff_counter)
            backoff_counter += 1
            continue
        except Exception as e:
            logger.print_nnl("ERROR!")
            logger.print_nnl("During processing \'" + user[1] + "\'.")
            logger.print_nnl("Tweet id was: \'" + str(last_id) + "\'.")
            logger.print_nnl(str(e))
            if str(e) == "Not authorized.":
                logger.print_nnl("NOT AUTHORIZED!!!")
                logger.print_nnl(user[1])
                logger.print_nnl(str(user[0]))
            break
    logger.print_nnl("Timeline of user {} id {} has ended.".format(user[1], user[0]))