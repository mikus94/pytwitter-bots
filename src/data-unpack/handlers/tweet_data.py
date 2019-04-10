# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
Application downloading tweets using Twitter API.
"""
"""
Module taking care of raw Twitter JSONs received by API.
"""
import time
import datetime

from configs.db_config import *
from .tools import *

def get_tweet_data(json):
    """
    Get regular tweet data.
    :param json: Get JSON containing Tweet JSON (Twitter API extended tweet).
    :returns: Shortened JSON of following structure.
        {
            # tweet id
            id,
            # tweeting user id
            user_id,
            # retweeted field from API
            retweeted,
            # date of creation tweet
            created_at,
            # text of message
            tweet,
            # language of tweet
            lang,
            # place if declared get only 'full_name' of JSON
            place,
            # number of retweet that tweet
            retweet_count,
            # number of favourites from API
            favourites_count,
            # appearance of hashtags, urls, medias and mentions
            entities
        }
    """
    tweet = {}

    for (field, default, func) in TT_FIELDS:
        # id from str
        if field == 'id':
            tweet['id'] = int(json['id_str'])
        # tweeting user id
        elif field == 'user_id':
            user_id = json['user'].get('id_str', '0')
            tweet['user_id'] = int(user_id)
        elif field == 'tweet':
            tweet['tweet'] = json['full_text']
        # place field is JSON. I only aim on full_name of location
        elif field == 'place':
            if json.get('place', None) is not None:
                tweet['place'] = json['place'].get('full_name', '')
            else:
                tweet['place'] = ''
        # the rest of fields
        else:
            tweet[field] = func(json.get(field, default))

    tweet['version'] = json['created_at']
    tweet['entities'] = get_entities(json['entities'])

    # check if any additional media was attached
    # ('native' media uploaded to twitter)
    extended = json.get('extended_entities', None)
    if extended is not None:
        extended_media = [
            (em['type'], em['media_url'])
            for em in extended.get('media', {})
        ]
        tweet['entities']['media'] = extended_media
    return tweet

def get_entities(json):
    """
    Getting entities like hashtags and user mentions.
    :param json: JSON containing entities.
    :returns: Shortened JSON of following structure.
        {
            'hashtags': [],
            'urls': [],
            'user_mentions': [(screen_name, user_ud)],
            'media': [(type, media_url)]
        }
    """
    # get all hashtags appearing in tweet
    hashtags = json['hashtags']
    hashtags = [h['text'] for h in hashtags]
    # get all urls
    urls = [u['expanded_url'] for u in json.get('urls', {})]
    # get all mentions
    user_mentions = [
        (um['screen_name'], int(um['id_str']))
        for um in json.get('user_mentions', {})
    ]
    media = [(m['type'], m['media_url']) for m in json.get('media', {})]
    entities = {
        'hashtags': hashtags,
        'urls': urls,
        'user_mentions': user_mentions,
        'media': media
    }
    return entities
