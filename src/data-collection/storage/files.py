# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
"""
import os
import json

from .singleton import Singleton

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

    def append_user_tweet(self, user, tweet):
        """
        Saving user tweet to its timeline.
        :param user: user id
        :param tweet: tweet
        """
        filepath = os.path.join(self.directory, user)
        with open(filepath, 'a') as f:
            # 1 tweet each line
            f.write(json.dumps(tweet, ensure_ascii=False))
            f.write('\n')

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