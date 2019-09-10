# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
"""
"""

"""
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle

from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier


import loader
from utilities import DESIRED_FIELDS

import numpy as np
np.set_printoptions(suppress=True)
np.set_printoptions(formatter={'all': lambda x: str(x)})

# CV
CV_NO = 10

"""
I ASSUME THAT 1 INDICATES BOT!!!!
0 = HUMAN!
"""

CLASSIFICATION_DATA = list(DESIRED_FIELDS)
# addition of time active field
CLASSIFICATION_DATA.append("time_active")
# indicate which fields are int
INT_FIELDS = range(1,6)

def split_labels(data):
    """
    Splitting data as label and data.
    """
    return data[:,0], data[:,1:]

def add_y(data, what):
    """
    Adding result column.
    """
    length = len(data)
    if what == 1:
        y = np.ones(length)
    else:
        y = np.zeros(length)
    res = ((np.c_[data, y]).astype(float))
    return res

def normalize(data):
    """
    Data normalization.
    """
    scaler = MinMaxScaler()
    return scaler.fit_transform(data)

def manipulate_data(data):
    """
    Function manipulating data
    :param data: prepared data.
    :return: manipulated data
    """

    def average_on_active(data):
        """
        Function that calculates average on active days (e.g. tweets no etc)).
        :param data:
        :return: averaged data
        """
        # index of column with active days
        active_index = CLASSIFICATION_DATA.index("time_active")
        # iterate on users
        for i in range(len(data)):
            time_delta = data[i,active_index]
            # iterate on integer fields
            # print("B4")
            # print(int(data[i,0]))
            # print(CLASSIFICATION_DATA)
            # print(data[i])
            for j in INT_FIELDS:
                data[i,j] = float(data[i,j] / time_delta)
            # print(data[i])
            # print("AFTER")
        return data

    data = average_on_active(data)
    return data

def drop_active_days(data):
    """
    Function dropping useless features.
    :param data: data
    :return: data without useless features
    """
    active_index = CLASSIFICATION_DATA.index("time_active")
    data = np.delete(data, active_index, 1)
    return data


################################################################################
# DATA LOADING
################################################################################

############ CRESCI

# cresci dataset
cresci_users = [
    'humans'
    # ,'social1'
    ,'social2'
    ,'social3'
    ,'traditional1'
    ,'traditional2'
    ,'traditional3'
    # ,'traditional4'
    # 'fake'
]
########## My data

# my collected data loading
(my_users_labels, my_users_data) = loader.load_exported_users('election')

########## CRESCI

# cresci data laoding
cresci_data = loader.load_cresci_users(cresci_users)


########## VAROL


# getting varol users data.
(varol_users_labels, varol_users_data) = loader.load_exported_users('varol')
# split varol data at bots and humans
varol_bots = varol_users_data[varol_users_labels[:,3] == 'True']
varol_humans = varol_users_data[varol_users_labels[:,3] == 'False']


# STUPID IDEA ITS MIXED?
# varol_humans = varol_users_data[varol_users_labels[:,3] == 'True']
# varol_bots = varol_users_data[varol_users_labels[:,3] == 'False']


######### CONCATENATION


# get humans data.
humans_cresci = cresci_data['humans']

# just cresci bots
bots_cresci = np.concatenate(
    [
        cresci_data[cresci_users[i]] 
        for i in range(1, len(cresci_users))
    ]
)


# with varol data
print("Boty\nCresci: {}\nVarol:{}\n".format(len(bots_cresci), len(varol_bots)))
print("Humany\nCresci: {}\nVarol:{}".format(len(humans_cresci), len(varol_humans)))


# Variants of humans / bots data usage.

# bots = varol_bots
bots = bots_cresci
# bots = np.concatenate([varol_bots, bots_cresci])

# humans = varol_humans
humans = humans_cresci
# humans = np.concatenate([varol_humans, humans_cresci])


print("\n\nUzyte\nBoty: {}\nHumany: {}".format(len(bots), len(humans)))


######### DATA PREPARATION

humans = humans.astype(np.float32)
bots = bots.astype(np.float32)
my_users_data = my_users_data.astype(np.float32)


# manipulation of data
# bots = manipulate_data(bots)
# humans = manipulate_data(humans)
# my_users_data = manipulate_data(my_users_data)


# drop active days column
# bots = drop_active_days(bots)
# humans = drop_active_days(humans)
# my_users_data = drop_active_days(my_users_data)


# skip label info for sets
_, bots = split_labels(bots)
_, humans = split_labels(humans)
_, my_users_data = split_labels(my_users_data)


# shuffle
h = shuffle(humans)
b = shuffle(bots)

# add y
h = add_y(h, 0.)
b = add_y(b, 1.)


def make_batches(data, no_batches):
    """
    Generate no_batches of data.
    """
    def make_batch_indecies(start_p, length, step):
        """
        Making batch indecies
        """
        return [ i for i in range(start_p, length, step)]

    indecies = []
    for i in range(no_batches):
        idx = make_batch_indecies(i, len(data), no_batches)
        indecies.append(idx)
    batches = []
    for idxes in indecies:
        batches.append(data[idxes])
    return batches


batches_b = make_batches(b, CV_NO)
batches_h = make_batches(h, CV_NO)

# concat data
batches_b = shuffle(batches_b)
batches_h = shuffle(batches_h)

batches = []
for bb, hh in zip(batches_b, batches_h):
    # concat humnas with bots
    concat = np.concatenate((bb, hh), axis=0)
    # shuffle them inside batch
    np.random.shuffle(concat)
    # add batch
    batches.append(concat)


def get_cv_data(batches, no):
    ttt = [i for i in range(CV_NO)]
    ttt.pop(no)
    bbb = [ batches[i] for i in ttt ]
    train = np.concatenate(bbb, axis=0)
    # placement of label
    # batch[0] - is batch
    # batch[0][0] - is element of batch
    label_place = len(batches[0][0]) - 1
    tr_x = train[:,:label_place]
    tr_y = train[:,label_place:].astype(int).flatten()
    tr_y = np.reshape(tr_y, (len(tr_y),))
    # test dataset
    test = batches[no]
    ts_x = test[:,:label_place]
    ts_y = test[:,label_place:].astype(int).flatten()
    ts_y = np.reshape(ts_y, (len(ts_y),))
    return tr_x, tr_y, ts_x, ts_y


def make_cv(clf, opts={}):
    scores = []
    for i in range(CV_NO):
        tr_x, tr_y, ts_x, ts_y = get_cv_data(batches, i)
        # print(tr_y)
        # clf = LogisticRegression(**log_opts)
        clf = clf.set_params(**opts)
        clf = clf.fit(tr_x, tr_y)
        sc = clf.score(ts_x, ts_y)
        scores.append(sc)

    print("Mean of " + str(CV_NO) + "-Cross-Validation.")
    print(np.mean(scores))


def classify(clf, opts={}, output='bots.txt'):
    clf = clf.set_params(**opts)

    # load whole training data for classifier
    train_data = np.concatenate([batches[i] for i in range(CV_NO)])
    label_place = len(batches[0][0]) - 1
    train_x = train_data[:,:label_place]
    train_y = np.reshape(train_data[:,label_place:].flatten(), (len(train_data),))

    # train
    clf = clf.fit(train_x, train_y)

    # predict
    predicts = clf.predict(my_users_data)

    # save
    ds = 0
    with open(output, 'w') as f:
        for label, udata, pred in zip(my_users_labels, my_users_data, predicts):
            if int(pred) == 1:
                ds += 1
                f.write(str(label))
                # f.write(str(udata))
                f.write('\n')

    print('\n==========================')
    print('Liczba botow')
    print(ds)
    print('na wszystkich uzytkownikow')
    print(len(my_users_data))
    print('Procent botow')
    print(ds/len(my_users_data))
    print('==========================')


# logistic regression options
log_opts = {
    'max_iter': 1000,
    'penalty': 'l2',
    # 'solver': 'liblinear'
    'solver': 'lbfgs'
}

clfs = [
    (LogisticRegression(), log_opts, 'LogisitcRegression', 'BotLog.txt'),
    (svm.LinearSVC(), {'max_iter': 10000}, 'SVM - LinearSVC', 'BotSvm.txt')
]

for clf, opts, name, output in clfs:
    print("\nClassification with {}.".format(name))
    make_cv(clf, opts)
    classify(clf, opts, output)
