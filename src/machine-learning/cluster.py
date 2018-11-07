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

from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


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


data = np.concatenate((b,h), axis=0)

data = shuffle(data)
data_ftrs = data[:,:data.shape[1]-1]
data_label = data[:,data.shape[1]-1:].flatten()

reduced_data = PCA(n_components=2).fit_transform(data_ftrs)
# reduced_data = PCA(n_components=2).fit_transform(my_users_data)

h = .02     # point in the mesh [x_min, x_max]x[y_min, y_max].

# Plot the decision boundary. For that, we will assign a color to each
x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
# xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))


plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)

plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
          'Centroids are marked with white cross')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())
plt.show()

exit()

# print(data.shape)
# print(data_ftrs.shape)
# print(data_label.shape)
# clf = KMeans(n_clusters=2).fit(data_ftrs)
# res = clf.labels_
# b = 0
# h = 0
# s = 0
# d = 0
# w1 = 0
# w2 = 0
# for l, r in zip(data_label, res):
#     if l == r:
#         s += 1
#         if l == 0:
#             # l 0
#             # r 0
#             # humany
#             h += 1
#         else:
#             # l 1
#             # r 1
#             # boty
#             b += 1
#     else:
#         d += 1
#         if l == 0:
#             # l 0
#             # r 1
#             w1 += 1
#         else:
#             # l 1
#             # r 0
#             w2 += 1

# print("REST")
# print("b {} \nh {} \ns {} \nd {} \nw1 {} \nw2 {}".format(b,h,s,d,w1,w2))


exit()


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
