# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
"""
"""

"""

import os
import datetime 
import csv
import numpy as np
np.set_printoptions(suppress=True)

import sklearn
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle

from sklearn.linear_model import LogisticRegression
from sklearn import svm


import loader

# CV
CV_NO = 10

"""
I ASSUME THAT 1 INDICATES BOT!!!!
0 = HUMAN!
"""


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

# cresci datasets to get
cresci_users = ['humans', 'social1', 'social2', 'traditional1', 'traditional2']

# cresci data laoding
cresci_data = loader.load_cresci_users(cresci_users)

# my collected data loading
(my_users_labels, my_users_data) = loader.load_my_users()
my_users_data = my_users_data[:,1:]
# my_users_data = normalize(my_users_data[:,1:])

humans = cresci_data['humans']


bots = np.concatenate(
    [
        cresci_data[cresci_users[i]] 
        for i in range(1, len(cresci_users))
    ]
)

_, bots = split_labels(bots)
_, humans = split_labels(humans)
# print(humans)
# exit()

# humans = normalize(humans)
# bots = normalize(bots)

# shuffle
h = shuffle(humans)
b = shuffle(bots)


# add y
h = add_y(h, 0)
b = add_y(b, 1)




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

scores = []
log_opts = {
    'max_iter': 500,
    'penalty': 'l2',
    # 'solver': 'liblinear'
    'solver': 'lbfgs'
}
for i in range(CV_NO):
    tr_x, tr_y, ts_x, ts_y = get_cv_data(batches, i)
    # print(tr_y)
    clf = LogisticRegression(**log_opts)
    # clf = svm.LinearSVC()
    clf = clf.fit(tr_x, tr_y)
    sc = clf.score(ts_x, ts_y)
    scores.append(sc)

print("\nMean of " + str(CV_NO) + "-Cross-Validation.")
print(np.mean(scores))


clf = LogisticRegression(**log_opts)
# clf = svm.LinearSVC()

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
with open('boty.txt', 'w') as f:
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
