# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
Application downloading tweets using Twitter API.
"""
"""
Module taking care of raw Twitter JSONs received by API.
"""

from .tweet_data import *
from .user_data import *

from .tools import *


def get_tweet(json):
    """
    Getting proper tweet.

    :param json: JSON parameter received from

    :returns: The return is json containing structure as below:
        {
            'user': 'Data of user that tweeted.'
            'tweet': 'Tweet data. Including retweet'
            'retweet': 'This field is filled with retweeted data. This is
                        available iff tweet was retweet.'
            'retweeted': Tweet data that was retweeted.
            'quoted': 'This field is fielld with quoted tweet. This is
                        available iff tweet was quoted tweet.'
            'quoted_tweet' Tweet data that was quoted.
        }
    """
    # get tweet and user
    tweet = get_tweet_data(json)
    version_date = datetime_to_date(tweet['created_at'])
    tweet['version'] = version_date
    user = get_user(json['user'])
    user['user']['version'] = version_date
    user['dsc_info']['version'] = version_date
    # create result
    result = {}
    result['tweet'] = tweet
    result['user'] = user
    # check whetver tweet is tweet, retweet or quote tweet.
    # retweet
    if (json.get('retweeted_status', None) is not None):
        # get retweeted tweet data
        retweeted = get_tweet_data(json.get('retweeted_status', {}))
        retweeted['version'] = version_date
        tweet['retweeted'] = True
################################################################################
####################### TODO: TURN OFF???! #####################################
################################################################################
        result['retweeted'] = retweeted
        # result['retweeted']['version'] = tweet['version']
        date = parse_time(json.get('created_at', None))
        result['retweet'] = {
            'id': tweet['id'],
            'tweet_id': retweeted['id'],
            'user_id': user['user']['id'],
            'created_at': date
        }
        return result
    # quoted
    elif ((json.get('is_quote_status', False) is True) and
            (json.get('quoted_status', None) is not None)):

        quoted_tweet = get_tweet_data(json.get('quoted_status', {}))
        quoted_tweet['version'] = version_date
################################################################################
####################### TODO: TURN OFF???! #####################################
################################################################################
        result['quoted_tweet'] = quoted_tweet
        # result['quoted_tweet']['version'] = tweet['version']
        result['quoted'] = {
            'id': tweet['id'],
            'quoted_id': quoted_tweet['id']
        }
        return result
    # regular tweet
    else:
        return result

def get_tweet_user(json):
    """
    Method extracting only user data from tweet.
    """
    return get_user(json)