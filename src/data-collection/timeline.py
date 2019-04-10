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
from time import sleep

from validator import Validator
from storage.files import FileHandler


# load config file
with open('config.json') as f:
    config_json = json.load(f)

# Validator of configuration file
validator = Validator()
validator.validate_downloader_config(config_json)


api_cred = config_json['twitter_api']

# create authentication objects
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

storage = FileHandler(config_json['data'])

users = config_json['timeline']['user_ids']

for user in users:
    # log user info
    msg = ("Start processing id: {} \n".format(user))
    print(msg)
    storage.append_log_file(msg)
    # opts
    count = 100
    search_opts = {
        'user_id': user,
        'count': 100
    }
    last_id=0
    backoff_counter = 1
    while True:
        try:
            for tweet in api.user_timeline(**search_opts):
                # get tweet data
                tweet_json = tweet._json
                last_id = tweet_json['id']
                # store data
                storage.append_user_tweet(str(user), tweet_json)
                count -= 1
                
            last_id=0
            break
        # check if error was ratelimit
        except tweepy.RateLimitError as e:
            # log error
            storage.append_log_error(user, last_id, e)
            print("Ratelimit!")
            # update search opts
            search_opts['max_id'] = int(last_id)
            search_opts['count'] = count
            # update backoff
            sleep(60*backoff_counter)
            backoff_counter += 1
            continue
        # check other errors
        except Exception as e:
            print("Exception!")
            storage.append_log_error(user, last_id, e)
            if str(e) == "Not authorized.":
                storage.append_log_info(user, str(e))
            break