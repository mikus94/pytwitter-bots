# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
"""

import os
import datetime

# get pwd
PWD = os.path.abspath(os.path.dirname(__file__))
DATA_COLLECTION_DIR = os.path.split(PWD)[0]
SRC_PATH = os.path.split(DATA_COLLECTION_DIR)[0]
# data is located at the same level as git repository
SRC_PATH = os.path.split(os.path.split(SRC_PATH)[0])[0]


# todays date@time
TODAY = str(datetime.date.today()) + "@" + str(datetime.datetime.today().time())
# create paths
# path to data
DATA = os.path.join(SRC_PATH, 'data')
# containing timelines of users
DATA_TIMELINES = os.path.join(DATA, 'timelines')
# containing directories with tweets splitted by (tweet, retweet, quote)
DATA_TT = os.path.join(DATA, 'content')
# containing only users data
DATA_USERS = os.path.join(DATA, 'users')
# containing raw responses from API
RAW_DATA = os.path.join(DATA, 'raw')
# tags
TAGS_PATH = os.path.join(DATA, 'tags')
# logs
LOG_PATH = os.path.join(DATA, 'logs')
