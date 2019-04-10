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
        :param arg: Output json config.
        """
        self.directory = arg['output_dir']
        self.filename = arg['filename']
        self.fullpath = os.path.join(self.directory, self.filename + '.txt')
        self.logpath = os.path.join(self.directory, self.filename + '.log')

        if os.path.exists(self.fullpath) or os.path.exists(self.logpath):
            print("Error!")
            print("There already exist \'{}\' output files.".format(self.filename))
            exit()
        # create output directory
        os.makedirs(self.directory, exist_ok=True)

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

    def append_raw_tweet(self, tweet):
        """
        Appending raw tweet to file.
        :param tweet: Tweet
        :return: None
        """
        with open(self.fullpath, 'a') as f:
            f.write(json.dumps(tweet))
            f.write('\n')

    def append_log_file(self, info):
        """
        Append some info to log file.
        :param info: Info to append.
        :return: None
        """
        with open(self.logpath, 'a') as f:
            f.write('\n' + info + '\n')

    def append_log_info(self, tag, msg):
        """
        Append log info.
        :param msg: Message to log.
        :param tag: Tag connected with message.
        :return: None
        """
        with open(self.logpath, 'a') as f:
            f.write('\nTag processing \'{}\'.\n'.format(tag))
            f.write(msg + '\n')

    def append_log_error(self, tag, last_id, error_msg):
        """
        Log errors.
        :param tag: Tag during which error occurred.
        :param last_id: Id of tweet when error occurred.
        :param error_msg: Error message.
        :return: None
        """
        with open(self.logpath, 'a') as f:
            f.write("\nERROR!\n")
            f.write("During processing \'" + tag + "\'.\n")
            f.write("Tweet id was: \'" + str(last_id) + "\'.\n")
            f.write(str(error_msg) + '\n\n')