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
from .db import DbHandler
from .files import FileHandler

class MultiStorage(metaclass=Singleton):
    """
    Class does both DB and file storage.
    """
    def __init__(self, arg, just_db=False):
        """
        Initialization
        :param arg: String to logging.
        :param just_db: Bool indicating if save also into the files.
        """
        self.just_db = just_db
        self.db = DbHandler()
        if not self.just_db:
            self.files = FileHandler(arg)

    def save(self, data):
        """
        Saving tweet data passed by JSON containing user, tweet and maybe
        retweet or quoted data.
        :param data: JSON obtained after unwrapping Twitter API JSON.
        """
        self.save_user(data['user'])
        if (data.get('tweet', None) is not None):
            self.save_tweet(data['tweet'])
        if (data.get('retweet', None) is not None):
            self.save_tweet(data['retweeted'])
            self.save_retweet(data['tweet'])
            self.save_my_retweet(data['retweet'])
        if (data.get('quoted', None) is not None):
            self.save_tweet(data['quoted_tweet'])
            self.save_quoted(data['tweet'])
            self.save_my_quoted(data['quoted'])

    def save_tweet(self, tweet):
        """
        Saving tweets in file system and db.
        :param tweet: My Tweet JSON.
        """
        self.db.insert_tweet(tweet)
        if not self.just_db:
            self.files.save_tweet(tweet)

    def save_retweet(self, retweet):
        """
        Saving retweet in file system and db
        :param retweet: My Retweet JSON.
        """
        self.db.insert_tweet(retweet)
        if not self.just_db:
            self.files.save_retweet(retweet)

    def save_my_retweet(self, retweet):
        """
        Saving retweet in file system and db
        :param retweet: My Retweet JSON.
        """
        self.db.insert_my_retweet(retweet)
        if not self.just_db:
            self.files.save_my_retweet(retweet)

    def save_quoted(self, quoted):
        """
        Saving quote in file system and db.
        :param quoted: My Quoted JSON.
        """
        self.db.insert_tweet(quoted)
        if not self.just_db:
            self.files.save_quoted(quoted)

    def save_my_quoted(self, quoted):
        """
        Saving quote in file system and db.
        :param quoted: My Quoted JSON.
        """
        self.db.insert_my_quoted(quoted)
        if not self.just_db:
            self.files.save_my_quoted(quoted)

    def save_user(self, user):
        """
        Saving user in file system and db.
        :param user: My User JSON.
        """
        self.db.insert_user(user)
        if not self.just_db:
            self.files.save_user(user)

    def save_raw_tweet(self, tweet):
        """
        Saving raw tweet json to file.
        :param tweet: Raw tweet json.
        """
        self.files.save_raw_tweet(tweet)

    def close(self):
        """
        Closing db connection.
        """
        self.db.close()