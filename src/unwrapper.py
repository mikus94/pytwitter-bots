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


def parse_time(time_str):
    """
    Parsing twitter time to python time.
    """
    ts = time.strftime(
        '%Y-%m-%d %H:%M:%S',
        time.strptime(
            time_str,
            '%a %b %d %H:%M:%S +0000 %Y'
        )
    )
    return ts


def get_tweet(json):
    """
    Getting proper tweet.

    :param json: JSON parameter received from

    :returns: The return is json containing structure as below:
        {
            'user': 'Data of user that tweeted.'
            'tweet': 'Tweet data. This field is not declared only with retweet.'
            'retweet': 'This field is filled with retweeted data. This is
                        available iff tweet was retweet.'
            'quoted': 'This field is fielld with quoted tweet. This is
                        available iff tweet was quoted tweet.'
        }
    """
    # get tweet and user
    tweet = get_tweet_data(json)
    user = get_user(json)
    # create result
    result = {}
    result['user'] = user
    # check whetver tweet is tweet, retweet or quote tweet.
    # retweet
    if (json.get('retweeted_status', None) is not None):
        # get retweeted tweet data
        retweeted = get_tweet_data(json.get('retweeted_status', {}))
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
        result['tweet'] = tweet
        result['quoted'] = {
            'id': tweet['id'],
            'quoted': quoted_tweet
        }
        return result
    # regular tweet
    else:
        result['tweet'] = tweet
        return result


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
    tweet['id'] = int(json['id_str'])
    tweet['user_id'] = int(json['user']['id_str'])

    tweet['retweeted'] = False

    tweet['created_at'] = parse_time(json['created_at'])
    tweet['tweet'] = json.get('full_text', '')
    tweet['lang'] = json.get('lang', '')
    # id declared get only full_name of localization
    if json.get('place', None) is not None:
        tweet['place'] = json['place'].get('full_name', '')
    else:
        tweet['place'] = ''
    tweet['retweet_count'] = json.get('retweet_count', 0)
    tweet['favourites_count'] = json.get('favourites_count', 0)
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


def get_user(json):
    """
    Getting user info out of tweet.
    Extracting information beeing used in following analizys.
    :param json: Tweet JSON which contains user informations.
    :returns: Shortened JSON of following structure.
    {
        user: {
                'id',
                'created_at',
                'screen_name',
                'default_profile',
                'default_profile_image',
                'profile_use_background_image',
                'statuses_count',
                'followers_count',
                'friends_count',
                'favourites_count',
                'listed_count',
                'geo_enabled',
                'verified',
                'protected',
                'version'
        },
        # additional info about user
        dsc_info: {
            'id',
            'description',
            'location',
            'lang',
            'version'
        }

    }
    """
    author_json = json['user']
    author = {}
    author_dsc = {}
    # id
    author['id'] = int(author_json['id_str'])
    author_dsc['id'] = int(author_json['id_str'])
    # created_at
    author['created_at'] = parse_time(author_json['created_at'])
    # lang
    author_dsc['lang'] = author_json.get('lang', 'xx')
    # profile attributes
    attributes_to_get = [
        # user name
        'screen_name',
        # profile attributes
        'default_profile',
        'default_profile_image',
        'profile_use_background_image',
        'statuses_count',
        'followers_count',
        'friends_count',
        'favourites_count',
        'listed_count',
        'geo_enabled',
        'verified',
        'protected',
    ]
    dsc_to_get = [
        'description',
        'location',
        'lang'
    ]
    for att in attributes_to_get:
        author[att] = author_json.get(att, '')
    for att in dsc_to_get:
        author_dsc[att] = author_json.get(att, '')
    today = str(datetime.date.today())
    author['version'] = today
    author_dsc['version'] = today
    # returning json with less data
    return {
        'user': author,
        'dsc_info': author_dsc
    }
