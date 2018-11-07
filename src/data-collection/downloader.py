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
import json
import datetime
import os
from time import sleep


from storage.multi import MultiStorage
from storage.logger import Logger

from configs import config
from configs.keywords import tags
from handlers import unwrapper


# create storage objects
storage = MultiStorage("downloader")
logger = Logger("downloader")

# start_date = '2018-10-12'
start_date = str(datetime.date.today() - datetime.timedelta(1))
end_date = str(datetime.date.today())

# variable storing count of all tweet data.
all_tts = 0

# create authentication objects
auth = tweepy.OAuthHandler(config.cost_key, config.cost_skey)
auth.set_access_token(config.acc_key, config.acc_skey)

# create API
api = tweepy.API(
    auth,
    wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True,
    retry_count=10,
    # retry_errors=[],
    retry_delay=5
)
for tag in tags:
    logger.tag_start(tag)
    # counters of (list below) for given tag
    # all tweets(tweet + retweet + quotes)
    # tweets
    # retweets
    # quote tweets
    all_no, tweet_no, retweet_no, quote_no = 0, 0, 0, 0
    cursor_opts = {
        'q':tag, 
        'count':100,
        'since':start_date,
        'until':end_date,
        'tweet_mode':'extended'
    }
    last_id=0
    backoff_counter = 1
    while True:
        try:
            for tweet in tweepy.Cursor(
                    api.search,
                    **cursor_opts
                ).items():

                all_no += 1
                # Checker that downloader did not stuck
                if (all_no % 100 == 0):
                    print("Already handled " + str(all_no) + " tweets.")
                # store raw tweet json
                storage.save_raw_tweet(tweet._json)
                # unwrap tweet
                unwrapped = unwrapper.get_tweet(tweet._json)
                # store unwrapped data
                storage.save(unwrapped)
                # count appereance of tweet type
                if unwrapped.get('retweet', None) is not None:
                    retweet_no += 1
                    last_id=unwrapped['retweet']['id']
                elif unwrapped.get('quoted', None) is not None:
                    quote_no += 1
                    last_id=unwrapped['quoted']['id']
                elif unwrapped.get('tweet', None) is not None:
                    tweet_no += 1
                    last_id=unwrapped['tweet']['id']
            last_id=0
            break
        except Exception as e:
            logger.print("ERROR!")
            logger.print("During processing \'" + tag + "\'.")
            logger.print("Tweet id was: \'" + str(last_id) + "\'.")
            logger.print(str(e))

            cursor_opts['max_id'] = int(last_id)

            sleep(60*backoff_counter)
            backoff_counter += 1
            continue

    # logger infos
    logger.tag_stats(tag, all_no, tweet_no, retweet_no, quote_no)
    logger.tag_finish(tag)
    # count everything
    all_tts += all_no

logger.download_info(start_date, end_date, tags, all_tts)
# close db
storage.close()