# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
"""
import psycopg2
import os
import json
import datetime

from .singleton import Singleton
from configs.data_config import *

class FileHandler(metaclass=Singleton):
    """
    Class handling storing data into the files.
    """

    def __init__(self, arg):
        """
        Init logger.
        :param arg: Subdirectory for data.
        """
        if arg in ['downloader', 'extractor']:
            self._init_downloader(arg)
        else:
            self._init_timeline()

    def _init_timeline(self):
        """
        Init timeline logger.
        """
        os.makedirs(DATA_TIMELINES, exist_ok=True)
        self.timeline = DATA_TIMELINES

    def _init_downloader(self, arg):
        """
        Init downloader/extractor
        """
        # create output dirs
        os.makedirs(RAW_DATA, exist_ok=True)

        # data split between downloader and extractor
        self.data_users = os.path.join(DATA_USERS, arg)
        self.data_tt = os.path.join(DATA_TT, arg)
        os.makedirs(self.data_users, exist_ok=True)

        self.path_t = os.path.join(self.data_tt, 'tweets')
        os.makedirs(self.path_t, exist_ok=True)
        
        self.path_r = os.path.join(self.data_tt, 'retweets')
        self.path_rt = os.path.join(self.path_r, 'tweet')
        self.path_mr = os.path.join(self.path_r, 'myretweet')
        os.makedirs(self.path_rt, exist_ok=True)
        os.makedirs(self.path_mr, exist_ok=True)
        
        self.path_q = os.path.join(self.data_tt, 'quotes')
        self.path_qt = os.path.join(self.path_q, 'tweet')
        self.path_mq = os.path.join(self.path_q, 'myquotes')
        os.makedirs(self.path_qt, exist_ok=True)
        os.makedirs(self.path_mq, exist_ok=True)

    def save_user_tweet(self, user, tweet):
        """
        Saving user tweet to its timeline.
        :param user: user id
        :param tweet: tweet
        """
        filepath = os.path.join(self.timeline, user)
        with open(filepath, 'a') as f:
            # 1 tweet each line
            f.write(json.dumps(tweet, ensure_ascii=False))
            f.write('\n')

    def format_json(self, data):
        """
        Formating json to desired output.
        """
        return json.dumps(data, indent=3, ensure_ascii=False)

    def save_json(self, path, filename, data):
        """
        Method printing json to desired file.
        """
        filepath = os.path.join(path, filename)
        with open(filepath, 'w') as f:
            f.write(self.format_json(data))

    def print_json(self, data):
        """
        Printing json to standard output.
        """
        print(self.format_json(data))

    def save_tweet(self, tweet):
        """
        Method saving tweets.
        """
        self.save_json(self.path_t, str(tweet['id']), tweet)

    def save_retweet(self, retweet):
        """
        Method saving retweets. Inside content/retweets/tweet
        """
        self.save_json(self.path_rt, str(retweet['id']), retweet)

    def save_my_retweet(self, retweet):
        """
        Method saving retweets. Inside content/retweets/myretweet
        """
        self.save_json(self.path_mr, str(retweet['id']), retweet)

    def save_quoted(self, quoted):
        """
        Method saving quotes. Inside content/quoted/tweet
        """
        self.save_json(self.path_qt, str(quoted['id']), quoted)

    def save_my_quoted(self, quoted):
        """
        Method saving quotes. Inside content/quoted/myquoted
        """
        self.save_json(self.path_mq, str(quoted['id']), quoted)

    def save_user(self, user):
        """
        Method saving users.
        """
        filename = (user['user']['screen_name'] + '@' + user['user']['version'])
        self.save_json(self.data_users, filename, user)

    def save_raw_tweet(self, tweet):
        """
        Saving raw Tweet.
        """
        self.save_json(RAW_DATA, str(tweet['id']), tweet)
