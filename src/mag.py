# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
Application downloading tweets using Twitter API.
"""
"""
Main module executing whole app.
"""
import tweepy
import json
import datetime
import os

from storage import MultiStorage, Logger

import config
import unwrapper
from keywords import tags

# create authentication objects
auth = tweepy.OAuthHandler(config.cost_key, config.cost_skey)
auth.set_access_token(config.acc_key, config.acc_skey)

# create API
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# create storage objects
storage = MultiStorage()
logger = Logger()

# start_date = str(datetime.date.today()) 
start_date = '2018-10-09'
end_date = str(datetime.date.today())

all_tts = 0
for tag in tags:
    logger.tag_start(tag)
    all_no, tweet_no, retweet_no, quote_no = 0, 0, 0, 0
    for tweet in tweepy.Cursor(
                    api.search, q=tag, count=100,
                    since=start_date, until=end_date,
                    tweet_mode='extended'
                ).items():

        all_no += 1
        if (all_no % 100 == 0):
            print("Already handled " + str(tt) + " tweets.")
        storage.save_raw_tweet(tweet._json)
        # unwrap tweet
        unwrapped = unwrapper.get_tweet(tweet._json)
        storage.save(unwrapped)
        # count appereance of tweet type
        if unwrapped.get('retweet', None) is not None:
            retweet_no += 1
        elif unwrapped.get('quoted', None) is not None:
            quote_no += 1
        elif unwrapped.get('tweet', None) is not None:
            tweet_no += 1

    logger.tag_stats(tag, all_no, tweet_no, retweet_no, quote_no)
    logger.tag_finish(tag)
    all_tts += all_no

logger.download_info(start_date, end_date, tags, all_tts)
storage.close_db()
