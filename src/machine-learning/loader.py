# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
"""
"""
Loading data module.
"""
import os
import datetime
import csv
import numpy as np
import sklearn

# path to data from DB
USER_DATA_PATH = '/home/miko/msc/trollemagisterka/src/data-collection/data/users.csv'

# path do cresci data
CRESCI_DATA = '/home/miko/msc/cresci-2017.csv/datasets_full.csv'

# fields needed to classifier
DESIRED_FIELDS = ["id", "statuses_count", "followers_count", "friends_count",
                    "favourites_count", "listed_count", "default_profile",
                    "geo_enabled", "profile_use_background_image", "verified",
                    "protected"
]

def convert_bool(cbool):
    """
    Converter converting byte string to bool.
    """
    cbool = cbool.decode('utf-8')
    if (cbool == 't'):
        return True
    else:
        return False

def str2date(x):
    """
    Convert date to numpy format.
    """
    return (datetime.datetime.strptime(x.decode("utf-8"), '%Y-%m-%d %H:%M:%S'))

def load_csv_np(filename):
    """
    Loads Cresci data to numpy.
    (Cant use genfromtxt cuz delimiter ',' exists in strings that 
    numpy cant handle them.)

    """
    res = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            res.append(row)

    res = np.asarray(res)
    header = res[0]
    res = res[1:]
    """
    TODO!
    UZYC HEADER ZAMIAST STATYCZNEJ LISTY
    """
    return header, res

def get_columns(which, data):
    """
    Getting desired columns out of Cresci data
    """
    # genuine accounts data
    genuine = ["id","name","screen_name","statuses_count","followers_count",
                "friends_count","favourites_count","listed_count","url","lang",
                "time_zone","location","default_profile",
                "default_profile_image","geo_enabled","profile_image_url",
                "profile_banner_url","profile_use_background_image",
                "profile_background_image_url_https","profile_text_color",
                "profile_image_url_https","profile_sidebar_border_color",
                "profile_background_tile","profile_sidebar_fill_color",
                "profile_background_image_url","profile_background_color",
                "profile_link_color","utc_offset","is_translator",
                "follow_request_sent","protected","verified","notifications",
                "description","contributors_enabled","following","created_at",
                "timestamp","crawled_at","updated","test_set_1","test_set_2"
    ]
    # social_spambots1
    social_spambots1 = ["id","name","screen_name","statuses_count",
                        "followers_count","friends_count","favourites_count",
                        "listed_count","url","lang","time_zone","location",
                        "default_profile","default_profile_image","geo_enabled",
                        "profile_image_url","profile_banner_url",
                        "profile_use_background_image",
                        "profile_background_image_url_https",
                        "profile_text_color","profile_image_url_https",
                        "profile_sidebar_border_color","profile_background_tile"
                        ,"profile_sidebar_fill_color",
                        "profile_background_image_url",
                        "profile_background_color","profile_link_color",
                        "utc_offset","is_translator","follow_request_sent",
                        "protected","verified","notifications","description",
                        "contributors_enabled","following","created_at",
                        "timestamp","crawled_at","updated","test_set_1"
    ]
    # socialspambots2
    social_spambots2 = ["id","name","screen_name","statuses_count",
                        "followers_count","friends_count","favourites_count",
                        "listed_count","url","lang","time_zone","location",
                        "default_profile","default_profile_image","geo_enabled",
                        "profile_image_url","profile_banner_url",
                        "profile_use_background_image",
                        "profile_background_image_url_https",
                        "profile_text_color","profile_image_url_https",
                        "profile_sidebar_border_color",
                        "profile_background_tile","profile_sidebar_fill_color"
                        ,"profile_background_image_url",
                        "profile_background_color","profile_link_color",
                        "utc_offset","is_translator","follow_request_sent",
                        "protected","verified","notifications","description",
                        "contributors_enabled","following","created_at",
                        "timestamp","crawled_at","updated"
    ]
    # social spambots 3
    social_spambots3 = ["id","name","screen_name","statuses_count",
                        "followers_count","friends_count","favourites_count",
                        "listed_count","url","lang","time_zone","location",
                        "default_profile","default_profile_image",
                        "geo_enabled","profile_image_url","profile_banner_url",
                        "profile_use_background_image",
                        "profile_background_image_url_https",
                        "profile_text_color","profile_image_url_https",
                        "profile_sidebar_border_color",
                        "profile_background_tile","profile_sidebar_fill_color",
                        "profile_background_image_url",
                        "profile_background_color","profile_link_color",
                        "utc_offset","is_translator","follow_request_sent",
                        "protected","verified","notifications","description",
                        "contributors_enabled","following","created_at",
                        "timestamp","crawled_at","updated","test_set_2"
    ]
    # traditional spambots 1
    traditional_spambots1 = ["id","name","screen_name","statuses_count",
                            "followers_count","friends_count",
                            "favourites_count","listed_count","url","lang",
                            "time_zone","location","default_profile",
                            "default_profile_image","geo_enabled",
                            "profile_image_url","profile_banner_url",
                            "profile_use_background_image",
                            "profile_background_image_url_https",
                            "profile_text_color","profile_image_url_https",
                            "profile_sidebar_border_color",
                            "profile_background_tile",
                            "profile_sidebar_fill_color",
                            "profile_background_image_url",
                            "profile_background_color",
                            "profile_link_color","utc_offset","is_translator",
                            "follow_request_sent","protected","verified",
                            "notifications","description",
                            "contributors_enabled","following","created_at",
                            "timestamp","crawled_at","updated"
    ]
    # traditional spambots 2
    traditional_spambots2 = ["id","name","screen_name","statuses_count",
                            "followers_count","friends_count",
                            "favourites_count","listed_count","url","lang",
                            "time_zone","location","default_profile",
                            "default_profile_image","geo_enabled",
                            "profile_image_url","profile_banner_url",
                            "profile_use_background_image",
                            "profile_background_image_url_https",
                            "profile_text_color","profile_image_url_https",
                            "profile_sidebar_border_color",
                            "profile_background_tile",
                            "profile_sidebar_fill_color",
                            "profile_background_image_url",
                            "profile_background_color",
                            "profile_link_color","utc_offset","is_translator",
                            "follow_request_sent","protected","verified",
                            "notifications","description",
                            "contributors_enabled","following",
                            "created_at","timestamp","crawled_at","updated"
    ]
    # traditional spambots 3
    traditional_spambots3 = ["id","name","screen_name","statuses_count",
                            "followers_count","friends_count",
                            "favourites_count","listed_count","url","lang",
                            "time_zone","location","default_profile",
                            "default_profile_image","geo_enabled",
                            "profile_image_url","profile_banner_url",
                            "profile_use_background_image",
                            "profile_background_image_url_https",
                            "profile_text_color","profile_image_url_https",
                            "profile_sidebar_border_color",
                            "profile_background_tile",
                            "profile_sidebar_fill_color",
                            "profile_background_image_url",
                            "profile_background_color","profile_link_color",
                            "utc_offset","is_translator","follow_request_sent",
                            "protected","verified","notifications",
                            "description","contributors_enabled",
                            "following","created_at","timestamp","crawled_at",
                            "updated"
    ]
    # traditional spambots 4
    traditional_spambots4 = ["id","name","screen_name","statuses_count",
                            "followers_count","friends_count",
                            "favourites_count","listed_count","url","lang",
                            "time_zone","location","default_profile",
                            "default_profile_image","geo_enabled",
                            "profile_image_url","profile_banner_url",
                            "profile_use_background_image",
                            "profile_background_image_url_https",
                            "profile_text_color","profile_image_url_https",
                            "profile_sidebar_border_color",
                            "profile_background_tile",
                            "profile_sidebar_fill_color",
                            "profile_background_image_url",
                            "profile_background_color","profile_link_color",
                            "utc_offset","is_translator","follow_request_sent",
                            "protected","verified","notifications",
                            "description","contributors_enabled","following",
                            "created_at","timestamp","crawled_at","updated"
    ]
    data_indecies = []
    if which == 'humans':
        data_indecies = genuine
    elif which == 'social1':
        data_indecies = social_spambots1
    elif which == 'social2':
        data_indecies = social_spambots2
    elif which == 'social3':
        data_indecies = social_spambots3
    elif which == 'traditional1':
        data_indecies = traditional_spambots1
    elif which == 'traditional2':
        data_indecies = traditional_spambots2
    elif which == 'traditional3':
        data_indecies = traditional_spambots3
    elif which == 'traditional4':
        data_indecies = traditional_spambots4
    else:
        print("WRONG DATASET NAME!!!! Given " + which)
        exit()

    indecies = [ data_indecies.index(d) for d in DESIRED_FIELDS ]
    data = data[:, indecies ]
    data[data==''] = '0'
    data[data=='NULL'] = '0'
    data = data.astype(int)
    return data

def load_my_users():
    # get data from csv (my tt data)
    # skip_header - skip header number of lines
    # names - indicate line after skip row containing names of columns
    # exclude_list - list of columns to skip
    # fname - file path
    # 8 - 13 t,fa 
    my_users = np.genfromtxt(
            fname=USER_DATA_PATH,
            delimiter=',',
            # usecols=[0, 1, 2,3,4,5,6,7,8,9,10,11,12,13],
            usecols=[i for i in range(14)],
            dtype=[
                np.dtype(int),
                np.dtype('U20'),
                # np.dtype(datetime.datetime), # date of creation account (STRING)
                np.dtype('U20'), # name of the account (20char string)
                np.dtype(int),
                np.dtype(int),
                np.dtype(int),
                np.dtype(int),
                np.dtype(int),
                np.dtype(bool),
                np.dtype(bool),
                np.dtype(bool),
                np.dtype(bool),
                np.dtype(bool),
                np.dtype(bool),
                np.dtype('M')
            ],
            # skiprows=1,
            names=True,
            # excludelist=['version'],
            converters={
                1: str2date,
                8: convert_bool,
                9: convert_bool,
                10: convert_bool,
                11: convert_bool,
                12: convert_bool,
                13: convert_bool,
                14: str2date
            }
    )

    # users labels
    users_labels = np.asarray([ (u[0], u[1], u[2]) for u in my_users ])
    # users data
    # obtain fields needed to classifier
    my_users = np.asarray([
        [
            u[d] for d in DESIRED_FIELDS
        ]
        for u in my_users
    ])
    return (users_labels, my_users)

def load_cresci_users(desired):
    """
    Loading cresci dataset
    """

    # cresci sets with their directory name
    cresci_sets = {
        'humans': 'genuine_accounts.csv',
        'social1': 'social_spambots_1.csv',
        'social2': 'social_spambots_2.csv',
        'social3': 'social_spambots_3.csv',
        'traditional1': 'traditional_spambots_1.csv',
        'traditional2': 'traditional_spambots_2.csv',
        'traditional3': 'traditional_spambots_3.csv',
        'traditional4': 'traditional_spambots_4.csv'
    }

    def load_one(name):
        """
        Load 1 dataset.
        """
        set_path = os.path.join(CRESCI_DATA, cresci_sets[name], 'users.csv')
        _, data = load_csv_np(set_path)
        data = get_columns(name, data)
        return data

    # result
    res = {}
    # load desired ones
    for d in desired:
        res[d] = load_one(d)
    return res