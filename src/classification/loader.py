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


from utilities import (
    DESIRED_FIELDS,
    CRESCI_FIELDS,
    VAROL_USER_DATA_PATH,
    USER_DATA_PATH,
    CRESCI_DATA
)


FEATURE_COLS = {}
for f, i in zip(DESIRED_FIELDS, range(len(DESIRED_FIELDS))):
    FEATURE_COLS[f] = i
FEATURE_COLS['activity'] = len(DESIRED_FIELDS)

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
    try:
        res = datetime.datetime.strptime(x.decode("utf-8"), '%Y-%m-%d %H:%M:%S')
    except AttributeError:
        res = datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    return (res)

def str2day(x):
    """
    Convert date to numpy format.
    """
    return (datetime.datetime.strptime(x.decode("utf-8"), '%Y-%m-%d'))
    

def get_active_days(dates_data):
    """
    Function getting active days of users.
    """
    # get appropriate date
    # dates_data = data[:,indices]
    # make vectorized function to convert date
    # make converter
    str2date_vect = np.vectorize(str2date)
    dates_data = str2date_vect(dates_data)
    # timedelta
    dates_data = dates_data[:,1] - dates_data[:,0]
    # function extracting days from datetime.deltatime object
    # +2 cuz of profiles that were active only 1 day
    days_vect = np.vectorize(lambda x: x.days + 2)
    # result
    dates_data = days_vect(dates_data)
    # reshape from ((X, )) to ((X, 1))
    dates_data = dates_data.reshape((len(dates_data), 1))
    return dates_data


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
    data_indecies = []
    if which == 'humans':
        data_indecies = CRESCI_FIELDS['genuine']
    elif which == 'social1':
        data_indecies = CRESCI_FIELDS['social_spambots1']
    elif which == 'social2':
        data_indecies = CRESCI_FIELDS['social_spambots2']
    elif which == 'social3':
        data_indecies = CRESCI_FIELDS['social_spambots3']
    elif which == 'traditional1':
        data_indecies = CRESCI_FIELDS['traditional_spambots1']
    elif which == 'traditional2':
        data_indecies = CRESCI_FIELDS['traditional_spambots2']
    elif which == 'traditional3':
        data_indecies = CRESCI_FIELDS['traditional_spambots3']
    elif which == 'traditional4':
        data_indecies = CRESCI_FIELDS['traditional_spambots4']
    elif which == 'fake':
        data_indecies = CRESCI_FIELDS['fake_followers']
    else:
        print("WRONG DATASET NAME!!!! Given " + which)
        exit()

    # extract days that account was active
    # get columns created_at and when was it crawled
    dates_indices = [ 
            # column timestamp correspond to created_at column.
            # it is the same date saved in timestamp format
            data_indecies.index(d) for d in ["timestamp", "crawled_at"]
        ]
    times_delta = get_active_days(data[:,dates_indices])

    # get desired data
    indecies = [data_indecies.index(d) for d in DESIRED_FIELDS]
    data = data[:,indecies]
    # fill missing data
    data[data==''] = '0'
    data[data=='NULL'] = '0'
    # concatenate active days data with data
    data = np.concatenate((data, times_delta), axis=1)
    data = data.astype(int)
    return data

def load_exported_users(which_users):
    """
    Loads my data exported from database to csv file.
    """
    # get data from csv (my tt data)
    # skip_header - skip header number of lines
    # names - indicate line after skip row containing names of columns
    # exclude_list - list of columns to skip
    # fname - file path
    # 8 - 13 t,fa 

    csv_dtype = [
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
                np.dtype('U20')
    ]

    csv_converters = {
                1: str2date,
                8: convert_bool,
                9: convert_bool,
                10: convert_bool,
                11: convert_bool,
                12: convert_bool,
                13: convert_bool,
                14: str2day
    }
    fname = ''
    no_cols = 1
    if which_users == 'election':
        fname = USER_DATA_PATH
        no_cols = 15
    elif which_users == 'varol':
        fname = VAROL_USER_DATA_PATH
        no_cols = 16
        csv_dtype.append(np.dtype(bool))
        csv_converters[15] = convert_bool
    else:
        print("ERROR!")
        print("WRONG TYPE OF DATA TO LOAD!")
        exit()

    my_users = np.genfromtxt(
            fname=fname,
            delimiter=',',
            names=True,
            usecols=[i for i in range(no_cols)],
            dtype=csv_dtype,
            converters=csv_converters
    )

    # users labels
    if which_users == 'election':
        users_labels = np.asarray([ (u[0], u[1], u[2]) for u in my_users ])
    else:
        # varol data
        # adding column indicating if user is bot
        users_labels = np.asarray([(u[0], u[1], u[2], u[15]) for u in my_users ])

    # getting active days
    time_delta = np.asarray([
        [
            (u[i]) for i in [1,14]
        ]
        for u in my_users
    ])
    time_delta = get_active_days(time_delta)

    # users data
    # obtain fields needed to classifier
    my_users = np.asarray([
        [
            u[d] for d in DESIRED_FIELDS
        ]
        for u in my_users
    ])
    my_users = np.concatenate((my_users, time_delta), axis=1)
    my_users.astype(int)
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
        'traditional4': 'traditional_spambots_4.csv',
        'fake': 'fake_followers.csv'
    }

    def load_one(name):
        """
        Load 1 dataset.
        """
        set_path = os.path.join(CRESCI_DATA, cresci_sets[name], 'users.csv')
        _, data = load_csv_np(set_path)
        data = get_columns(name, data)
        data.astype(int)
        return data

    # result
    res = {}
    # load desired ones
    for d in desired:
        res[d] = load_one(d)
    return res
