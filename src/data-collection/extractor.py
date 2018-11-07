# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
Application downloading tweets using Twitter API.
"""
"""
Extracting from raw module.
"""
import getopt
import sys

import json
import datetime
import os

from storage import MultiStorage, Logger
from handlers import unwrapper

from configs.data_config import *


def format_json(data):
    """
    Formating json to desired output.
    """
    return json.dumps(data, indent=3, ensure_ascii=False)

def main(path, opts):
    """
    Extract stores
    """
    # create logger
    logger = Logger("extractor")
    storage = MultiStorage("extractor", True)

    if opts.get('store', 'single') == 'multi':
        # I ASSUME THIS IS DIR OF DATAs
        all_datas = os.listdir(path)
        for store in all_datas:
            store_path = os.path.join(path, store, 'raw')
            one_store(store_path, logger, storage)
    else:
        one_store(path, logger, storage)

    storage.close()

def one_store(path, logger, storage):
    """
    Extract one strage
    """

    files = os.listdir(path)
    # files
    print("Processing:")
    print(path)
    print(len(files))
    all_tweets_no = len(files)
    counter = 0
    for f in files:
        # path to file
        filepath = os.path.join(path, f)
        # load tweet
        with open(filepath, 'r') as fd:
            tweet = json.load(fd)
        counter += 1
        unwrapped = unwrapper.get_tweet(tweet)
        storage.save(unwrapped)
        if counter % 250 == 0:
            print(
                """From store \'{}\'\n
                Already {} tweets out of {} handled."""
                .format(path, str(counter), str(all_tweets_no))
            )
            print("Percentage: {}%.".format(str((counter / all_tweets_no)*100)))

        

def usage():
    print("To exectute insert -p option with path to raw tweet files.")
    print(
        "You need also declare if you want to store your extracted tweets in:\n\
        -Database -d option.\n\
        -Directory -f and you need to apply correct path."
    )

def check_path(path):
    """
    Checking if path is correct.
    :param path: Path to directory containing tweets.
    """
    if not os.path.exists(path):
        print("Error!")
        print("Given path: \'{}\' is not correct!".format(path))
        exit(2)
    if not os.path.isdir(path):
        print("Error!")
        print("Given path: \'{}\' is not directory!".format(path))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error!")
        print("Too few arguments passed!\n")
        usage()
        exit(2)
    path = sys.argv[1]
    
    try:
        # opts, args = getopt.getopt(sys.argv[1:], "p:f:d")
        opts, args = getopt.getopt(sys.argv[1:], "p:d:")
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    # parse options
    input_dir = False
    output_opt = False
    print(opts)
    for opt, arg in opts:
        # path declaration
        if opt == '-p':
            if arg != '':
                input_dir = True
                path = arg
                check_path(path)
                store_opt = {
                    'store': 'single'
                }
            else:
                print("ERROR!")
                print("You need to declare path for -p option!")
                exit()
        elif opt == '-d':
            if arg != '':
                input_dir = True
                path = arg
                check_path(path)
                store_opt = {
                    'store': 'multi'
                }
            else:
                print("ERROR!")
                print("You need to declare path for -d option!")
                exit()
        # store in DB
        # elif opt == '-d':
        #     output_opt = True
        #     store_opt = {
        #         'opt': 'database'
        #     }
        # store in files
        # elif opt == '-f':
        #     if arg != '':
        #         output_opt = True
        #         store_opt = {
        #             'opt': 'file',
        #             'path': arg
        #         }
        #     else:
        #         print("Error!")
        #         print("Option -f require argument!")
        #         exit()
    if not input_dir:
        print("Error!")
        print("You need to declare input direcory!\n")
        usage()
        exit()
    # if not output_opt:
    #     print("Error!")
    #     print("You need to declare output option!\n")
    #     usage()
    #     exit()

    # execute extraction
    main(path, store_opt)