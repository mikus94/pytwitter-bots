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
import glob

from storage import MultiStorage
from handlers import unwrapper
from handlers.tools import parse_time, datetime_to_date

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
    storage = MultiStorage("extractor", True)

    option = opts.get('store', 'single')
    if option == 'multi-gathered':
        # extracting multiple storage files with multiple jsons.
        # all_datas = os.listdir(path)
        all_datas = glob.glob(path + '/*.dat')
        for store in all_datas:
            store_path = os.path.join(path, store)
            multiple_extraction(store_path, storage)
    elif option == 'varol':
        # extract varol dataset
        store_varol(path, storage)

    storage.close()

def store_varol(path, storage):
    """
    Extracting and saving varol user dataset.
    """
    print("Processing Varol dataset at: {}".format(path))
    # read file
    with open(path, 'r', encoding='utf-8') as f:
        full_data = f.readlines()
    all_users_no = len(full_data)
    print(all_users_no)
    counter = 0
    # load each user
    for line in full_data:
        # just 1 split
        # data is like (bot_indent) space json
        # if not declared breaks json
        line = line.strip().split(maxsplit=1)
        bot_or_not = line[0]
        tweet = json.loads(line[1])
        counter += 1
        unwrapped = unwrapper.get_tweet_user(tweet)

        if tweet.get('status', None) is None:
            version = str(datetime.date.today())
        else:
            version = datetime_to_date(parse_time(tweet['status']['created_at']))
        unwrapped['user']['version'] = version
        unwrapped['user']['bot'] = bot_or_not
        storage.save_varol_user(unwrapped)
        # print progress of users loading
        progress_print(counter, path, all_users_no)
    pass

def multiple_extraction(path, storage):
    """
    Extract just 1 file containing multiple jsons with tweet data.
    """
    print("Processing: {}".format(path))
    print(path)
    # read whole file
    with open(path, 'r', encoding='utf-8') as f:
        full_data = f.readlines()
    print(len(full_data))
    all_tweets_no = len(full_data)
    counter = 0
    # iterate over tweets
    for line in full_data:
        # erase unnecesairy whitespaces
        line = line.strip()
        # load json
        tweet = json.loads(line)
        counter += 1
        unwrapped = unwrapper.get_tweet(tweet)
        storage.save(unwrapped)
        # print progress
        progress_print(counter, path, all_tweets_no)


def progress_print(counter, path, all_tweets_no):
    if counter % 500 == 0:
            print(
                """From store \'{}\'\n
                Already {} tweets out of {} handled."""
                .format(path, str(counter), str(all_tweets_no))
            )
            print("Percentage: {}%.".format(str((counter / all_tweets_no)*100)))

def usage():
    print(
        "Usage information.\n"
        "(*) We assume that Tweet jsons are gathered in single file with "
        "'*.dat' extension.\n"
        "(*) Moreover single line contain single tweet.\n"
        "Execution:\n"
        "- to execute insertion file with many tweets use option '-p'.\n"
        "- to execute insertion of Varol dataset users use option '-v'.\n"
    )


def check_path(path, check_dir=False):
    """
    Checking if path is correct.
    :param path: Path to directory containing tweets.
    """
    if not os.path.exists(path):
        print("Error!")
        print("Given path: \'{}\' is not correct!".format(path))
        exit(2)
    if check_dir and not os.path.isdir(path):
        print("Error!")
        print("Given path: \'{}\' is not directory!".format(path))

if __name__ == "__main__":
    # check if option is declared with path
    if len(sys.argv) < 2:
        print("Error!")
        print("Too few arguments passed!\n")
        usage()
        exit(2)

    # get path
    path = sys.argv[1]

    # try options
    try:
        # opts, args = getopt.getopt(sys.argv[1:], "p:f:d")
        opts, args = getopt.getopt(sys.argv[1:], "p:v:")
    # wrong options
    # print help information and exit:
    except getopt.GetoptError as err:
        # will print something like "option -a not recognized"
        print(err, '\n')
        usage()
        sys.exit(2)

    # parse options
    input_dir = False
    output_opt = False
    print(opts)
    store_opt={}
    # execution option
    for opt, arg in opts:
        # path declaration
        if opt == '-p':
            if arg != '':
                input_dir = True
                path = arg
                check_path(path)
                store_opt = {
                    'store': 'multi-gathered'
                }
            else:
                print("ERROR!")
                print("You need to declared path for -p option!")
                exit()
        elif opt == '-v':
            if arg != '':
                input_dir = True
                path = arg
                check_path(path)
                store_opt = {
                    'store': 'varol'
                }
            else:
                print("ERROR!")
                print("You need to declare path for -v option!")
                exit()
        
    if not input_dir:
        print("Error!")
        print("You need to declare input direcory!\n")
        usage()
        exit()

    # execute extraction
    main(path, store_opt)