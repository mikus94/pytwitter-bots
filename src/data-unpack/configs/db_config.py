# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
"""
import datetime
from .tools import *

_TODAY = str(datetime.date.today())

# configuration of connection to DB
DB_CONNECTION = ("""
    dbname='twitter'
    user='postgres'
    host='localhost'
    password='1234'
""")

################################################################################
# fields that are required to DB table + its default values + parsing function
################################################################################
_FUNC_ID_ = lambda x: x
_FUNC_INT_ = lambda x: int(x)
_FUNC_DATE_ = lambda x: parse_time(x)

# tweets
TT_TABLE = 'tweet'
TT_FIELDS = [
    ('id', 0, _FUNC_INT_),
    ('created_at', '1994-01-01', _FUNC_DATE_),
    ('tweet', '', _FUNC_ID_),
    ('retweeted', False, _FUNC_ID_),
    ('retweet_count', 0, _FUNC_INT_),
    ('favorite_count', 0, _FUNC_INT_),
    ('lang', '', _FUNC_ID_),
    ('user_id', 0, _FUNC_INT_),
    ('version', _TODAY, _FUNC_ID_),
    ('place', '', _FUNC_ID_)
]

# users
USR_TABLE = 'twitter_user'
USR_FIELDS = [
    ('id', 0, _FUNC_INT_),
    ('created_at', '1994-01-01', _FUNC_DATE_),
    ('screen_name', 'XXX', _FUNC_ID_),
    ('statuses_count', 0, _FUNC_INT_),
    ('followers_count', 0, _FUNC_INT_),
    ('friends_count', 0, _FUNC_INT_),
    ('favourites_count', 0, _FUNC_INT_),
    ('listed_count', 0, _FUNC_INT_),
    ('geo_enabled', False, _FUNC_ID_),
    ('verified', False, _FUNC_ID_),
    ('protected', False, _FUNC_ID_),
    ('default_profile', True, _FUNC_ID_),
    ('profile_use_background_image', True, _FUNC_ID_),
    ('default_profile_image', True, _FUNC_ID_),
    ('version', _TODAY, _FUNC_ID_)
]

# user description
USR_DSC_TABLE = 'twitter_user_dsc'
USR_DSC_FIELDS = [
    ('id', 0, _FUNC_INT_),
    ('description', '', _FUNC_ID_),
    ('location', '', _FUNC_ID_),
    ('lang', '', _FUNC_ID_),
    ('version', _TODAY, _FUNC_ID_)
]

# varol data
VAROL_USR_TABLE = 'varol_user'
VAROL_USR_FIELDS = [
    ('id', 0, _FUNC_INT_),
    ('created_at', '1994-01-01', _FUNC_DATE_),
    ('screen_name', 'XXX', _FUNC_ID_),
    ('statuses_count', 0, _FUNC_INT_),
    ('followers_count', 0, _FUNC_INT_),
    ('friends_count', 0, _FUNC_INT_),
    ('favourites_count', 0, _FUNC_INT_),
    ('listed_count', 0, _FUNC_INT_),
    ('geo_enabled', False, _FUNC_ID_),
    ('verified', False, _FUNC_ID_),
    ('protected', False, _FUNC_ID_),
    ('default_profile', True, _FUNC_ID_),
    ('profile_use_background_image', True, _FUNC_ID_),
    ('default_profile_image', True, _FUNC_ID_),
    ('version', _TODAY, _FUNC_ID_),
    ('bot', False, _FUNC_ID_)
]


# hashtags
HASH_TABLE = 'hashtag'
HASH_FIELDS = [
    ('tweet_id', 0, _FUNC_INT_),
    ('tag', '', _FUNC_ID_)
]

# mentions
MENTIONS_TABLE = 'mentions'
MENTIONS_FIELDS = [
    ('tweet_id', 0, _FUNC_INT_),
    ('user_id', 0, _FUNC_INT_)
]

# urls
URLS_TABLE = 'urls'
URLS_FIELDS = [
    ('tweet_id', 0, _FUNC_INT_),
    ('link', '', _FUNC_ID_)
]

# media
MEDIA_TABLE = 'media'
MEDIA_FIELDS = [
    ('tweet_id', 0, _FUNC_INT_),
    ('type', '', _FUNC_ID_),
    ('link', '', _FUNC_ID_)
]

# retweets
RTT_TABLE = 'retweets'
RTT_FIELDS = [
    ('id', 0, _FUNC_INT_),
    ('tweet_id', 0, _FUNC_INT_),
    ('user_id', 0, _FUNC_INT_),
    ('created_at', '1994-01-01', _FUNC_DATE_)
]

# quotes
QTT_TABLE = 'quotes'
QTT_FIELDS = [
    ('id', 0, _FUNC_INT_),
    ('quoted_id', 0, _FUNC_INT_)
]