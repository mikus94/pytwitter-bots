# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
"""
import os
import datetime 
import csv
import numpy as np

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


import psycopg2

DB_CONNECTION = ("""
    dbname='twitter'
    user='postgres'
    host='localhost'
    password='1234'
""")



# connect

try:
    conn = psycopg2.connect(DB_CONNECTION)
    # self.conn = psycopg2.connect(DB_TEST)
    cur = conn.cursor()
except Exception as e:
    print("I am unable to connect to the database, due to\n")
    print(e)
    exit()

sql_timeline = """
                SELECT E.t, E.c 
                FROM (
                    SELECT  date_trunc('hour', created_at) as t, count(1) as c 
                    FROM tweet  
                    GROUP BY 1
                    ) as E 
                WHERE E.t>'2018-10-05 00:00:00';
                """


# cur.execute("""SELECT DISTINCT created_at FROM tweet ORDER BY created_at;""")
cur.execute(sql_timeline)
data = cur.fetchall()
xs = []
ys = []
for t in data:
    # print(str(t[0]), ' ', str(t[1]))
    xs.append(str(t[0]))
    ys.append(t[1])


days = mdates.DayLocator(interval=4)
days.MAXTICKS = 4000
# days = mdates.DayLocator()
hours = mdates.HourLocator(byhour=[6, 12, 18])
hours.MAXTICKS = 40000

# plt.plot_date(x=xs, y=ys, fmt="g-")
# plt.title("Pageessions on example.com")
# plt.ylabel("Page impressions")
# plt.grid(True)
# plt.show()

fig, ax = plt.subplots()

# # format the ticks
print(ax.xaxis.get_major_locator())
ax.xaxis.set_major_locator(days)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)
print(ax.xaxis.get_major_locator())


# ax.xaxis.set_minor_locator(hours)
# ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H:%M"))
# plt.setp(ax.xaxis.get_minorticklabels(), rotation=90)


# # format the coords message box
# ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
# ax.format_ydata = lambda x: x
ax.grid(True)

# # rotates and right aligns the x labels, and moves the bottom of the
# # axes up to make room for them
# fig.autofmt_xdate()

ax.plot(xs, ys)
plt.show()