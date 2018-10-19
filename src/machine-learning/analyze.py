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

import sklearn
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import shuffle

from sklearn.linear_model import LogisticRegression
from sklearn import svm


import loader

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

# humans = normalize(humans)
# bots = normalize(bots)

# shuffle
h = shuffle(humans)
b = shuffle(bots)


# add y
h = add_y(h, 0)
b = add_y(b, 1)



# CV
cv_no = 10
h_len = len(h) / cv_no
b_len = len(b) / cv_no
print("data len")
print(len(h))
print(len(b))

batches = {}
for i in range(cv_no):
    start_h = int(i * h_len)
    end_h = int((i+1) * h_len )
    start_b = int(i * b_len)
    end_b = int((i+1) * b_len)
    # batch
    if i != cv_no - 1:
        hs = h[start_h:end_h]
        bs = b[start_b:end_b]
        batch = np.r_[bs, hs]
    else:
        hs = h[start_h:]
        bs = b[start_b:]
        batch = np.r_[bs, hs]
    batch = shuffle(batch)
    batches[str(i)] = batch


# for k,v in batches.items():
#     print(k)
#     print(len(v))

def get_cv_data(batches, no):
    # if no == 0:
    #     train = batches[str(cv_no-1)]
    # else:
    #     train = batches['0']
    # for i in range(1,cv_no-1):
    #     if i != no:
    #         train = np.r_[train, batches[str(i)]]
    ttt = [i for i in range(cv_no)]
    ttt.pop(no)
    # print(ttt)
    bbb = [ batches[str(i)] for i in ttt ]
    train = np.concatenate(bbb, axis=0)
    # print(train.shape)
    tr_x = train[:,:10]
    tr_y = train[:,10:].astype(int).flatten()
    tr_y = np.reshape(tr_y, (len(tr_y),))
    test = batches[str(no)]
    ts_x = test[:,:10]
    ts_y = test[:,10:].astype(int).flatten()
    ts_y = np.reshape(ts_y, (len(ts_y),))
    return tr_x, tr_y, ts_x, ts_y

scores = []
log_opts = {
    'max_iter': 500,
    'penalty': 'l2',
    'solver': 'liblinear'
    # 'solver': 'lbfgs'
}
for i in range(cv_no):
    tr_x, tr_y, ts_x, ts_y = get_cv_data(batches, i)
    # print(tr_x.shape)
    # print(tr_y.shape)
    # print(tr_y)
    clf = LogisticRegression(**log_opts)
    # clf = svm.LinearSVC()
    clf = clf.fit(tr_x, tr_y)
    sc = clf.score(ts_x, ts_y)
    scores.append(sc)

print("\nMean of " + str(cv_no) + "-Cross-Validation.")
print(np.mean(scores))
clf = LogisticRegression(**log_opts)
# clf = svm.LinearSVC()
# load whole training data for classifier
train_data = np.concatenate([batches[str(i)] for i in range(cv_no)])
train_x = train_data[:,:10]
train_y = np.reshape(train_data[:,10:].flatten(), (len(train_data),))

clf = clf.fit(train_x, train_y)

ds = 0
predicts = clf.predict(my_users_data)
with open('boty.txt', 'w') as f:
    for label, pred in zip(my_users_labels, predicts):
        if int(pred) == 1:
            ds += 1
            f.write(str(label))
            f.write('\n')

print('Liczba botow')
print(ds)
print('na wszystkich uzytkownikow')
print(len(my_users_data))
