# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
Application downloading tweets using Twitter API.
"""
"""
Downloading module.
"""
from validator import Validator

from storage.files import FileHandler

import tweepy
from time import sleep
import json

# load config file
with open('config.json') as f:
    config_json = json.load(f)

# Validator of configuration file
validator = Validator()
validator.validate_downloader_config(config_json)

# create storage objects
storage = FileHandler(config_json['data'])

# variable storing count of tweets downloaded.
all_tts = 0

# create authentication objects
api_cred = config_json['twitter_api']
auth = tweepy.OAuthHandler(api_cred['cost_key'], api_cred['cost_skey'])
auth.set_access_token(api_cred['acc_key'], api_cred['acc_skey'])

# create API
api = tweepy.API(
    auth,
    wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True,
    retry_count=10,
    retry_delay=5
)

# get cursor opts
tags = config_json['cursor']['keywords']
start_date = config_json['cursor']['since']
end_date = config_json['cursor']['until']

# start logging
storage.append_log_file('Processing keywords:\n {} '.format(tags))

# download tweets by tags
for tag in tags:
    msg = 'Starting processing tag.'
    storage.append_log_info(tag, msg)
    print('Processing {}'.format(tag))
    all_no = 0
    # set current cursor options
    cursor_opts = {
        'q': tag,
        'count': 100,
        'since': start_date,
        'until': end_date,
        'tweet_mode': 'extended'
    }
    # rest last_id and backoff_counter
    last_id = 0
    backoff_counter = 1
    while True:
        try:
            for tweet in tweepy.Cursor(
                    api.search,
                    **cursor_opts
                    ).items():

                all_no += 1
                # Checker that downloader did not stuck
                if all_no % 100 == 0:
                    print("Already handled " + str(all_no) + " tweets.")
                # store raw tweet json
                storage.append_raw_tweet(tweet._json)
                # update last_id
                last_id = tweet._json['id']
            # all of the tweets (by keyword) downloaded
            break
        # there was rate limit
        except Exception as e:
            # log error
            storage.append_log_error(tag, last_id, str(e))
            # print error to stdout
            print('Error\nDuring processing \'{}\'.\n'.format(tag))
            print('Last Tweet id was: {}\n'.format(last_id))
            print(str(e))
            # point last tweet downloaded
            cursor_opts['max_id'] = last_id
            # sleep till rate limit is handled
            sleep(60*backoff_counter)
            backoff_counter += 1
            continue

    # logger infos
    msg = ('Processing finished with {} tags'.format(all_no))
    storage.append_log_info(tag, msg)
    # count everything
    all_tts += all_no

storage.append_log_file('There was {} all tweets.'.format(all_tts))