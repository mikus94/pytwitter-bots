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

class Logger(metaclass=Singleton):
    """
    Class that writes logs about computation into the file. It also prints info
    on standard output.
    """
    def __init__(self, arg):
        """
        Initialization of logger.
        """
        # split of loggs
        self.log_path = os.path.join(LOG_PATH, arg)

        if arg in ['downloader', 'extractor']:
            self.tags_path = os.path.join(TAGS_PATH, TODAY)
            os.makedirs(self.tags_path, exist_ok=True)
        
        os.makedirs(self.log_path, exist_ok=True)
        
        self.log_path = os.path.join(self.log_path, TODAY)


    def tag_stats(self, tag, all_tt, tt, rt, qt):
        """
        Log info about downloading given tag.
        :param tag: String containing tag.
        :param tt: Integer determining number tweets containing given tag.
        :param rt: Integer determining number of retweets of tweets with given
            tag.
        "param qt: Integer determining number of quoted tweets containing tag.
        """
        all_tts = "All actions: " + str(all_tt)
        tts = 'Tweets: ' + str(tt)
        rts = 'Retweets: ' + str(rt)
        qts = 'Quoted: ' + str(qt)
        # log to file
        with open(os.path.join(self.tags_path, tag), 'w') as f:
            f.write(tag + '\n')
            f.write(all_tts + '\n')
            f.write(tts + '\n')
            f.write(rts + '\n')
            f.write(qts + '\n')
        # log to stdout
        log = (
            "Tag \'" + tag + "\' info:\n{" + 
            all_tts + ", " + tts + ", " + rts + ", " + qts + "}"
        )
        print(log)
        with open(self.log_path, 'a') as f:
            f.write(log + '\n')

    def tag_start(self, tag):
        """
        Log info about begining of diggig.
        :param tag: String with tag.
        """
        log = "\'" + tag + "\'\n"
        log = log + "Start digging \'" + tag + "\'."
        with open(self.log_path, 'a') as f:
            f.write(log + '\n')
        print(log)

    def tag_finish(self, tag):
        """
        Log info about finished digging.
        :param tag: String with tag.
        """
        log = "Finished digging tag: \'" + tag + "\'."
        with open(self.log_path, 'a') as f:
            f.write(log + '\n\n')
        print(log + '\n')

    def download_info(self, since, until, tags, no_data):
        """
        Logging info about digging process.
        :param since: Date indicating start point of digging tweets.
        :param until: Date indicating end point of digging tweets.
        :param tags: List of tags that were digged.
        :param no_data: Number of tweets digged.
        """
        log = (
            "End of downloading. In total there were " + str(no_data) +
            " tweets downloaded.\n" +
            "These tweets were posted from " + str(since) + " to " +
            str(until) + "."
        )
        print("\n" + log + "\n")
        with open(self.log_path, 'a') as f:
            f.write('==================================' + '\n')
            f.write(log + '\n')
            f.write("Tags downloaded are listed below." + '\n')
            f.write(str(tags) + '\n')
            f.write('==================================' + '\n')

    def print(self, txt):
        """
        Print into logger file and stdout.
        :param txt: text to print in.
        """
        print(txt)
        with open(self.log_path, 'a') as f:
            f.write('\n')
            f.write(txt + '\n')
            f.write('\n')

    def print_nnl(self, txt):
        """
        Print into logger file and stdout.
        :param txt: text to print in.
        """
        print(txt)
        with open(self.log_path, 'a') as f:
            f.write(txt + '\n')