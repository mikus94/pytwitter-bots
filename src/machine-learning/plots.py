# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
Plotting module.
"""
from config import DB_CONNECTION, PLOTS_DIR

import os
import numpy as np
import psycopg2

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
matplotlib.use('PS')

# COLORS
KO_COLOR = 'orange'
KO_COLOR_SUPP = 'peachpuff'
KO_COLOR_SUSP = 'tan'
KO_DELETED_COLOR = 'slategrey'

PIS_COLOR = 'blue'
PIS_COLOR_SUPP = 'deepskyblue'
PIS_COLOR_SUSP = 'cyan'
PIS_DELETED_COLOR = 'rosybrown'

JOURNALIST_COLOR = 'green'


def get_data(sql):
    """
    Function returning results from DB. SQLs returning 2 fields index and value.
    :param sql: SQL query
    :return: Returns 2 arrays (Indexes, Values).
    """
    # connect
    try:
        conn = psycopg2.connect(DB_CONNECTION)
        # self.conn = psycopg2.connect(DB_TEST)
        cur = conn.cursor()
        # execute
        cur.execute(sql)
        data = cur.fetchall()
        xs = []
        ys = []
        for t in data:
            xs.append((t[0]))
            ys.append(t[1])
        cur.close()
        return xs, ys
    except Exception as e:
        print("I am unable to connect to the database, due to\n")
        print(e)
        exit()


def get_all_tweets():
    """
    Function producing plot of overall tweets posted during investigated time.
    :return: None
    """
    sql = """
            SELECT E.t, E.c
            FROM (
                SELECT  date_trunc('hour', created_at) as t, count(1) as c
                FROM tweet
                GROUP BY t
                ) as E
            WHERE E.t>'2018-10-05 00:00:00';
        """

    xs, ys = get_data(sql)

    # create figure/plot
    fig, ax = plt.subplots()

    # configure tickers
    day = mdates.DayLocator()  # every day
    time_fmt = mdates.DateFormatter('%d-%m-%Y')

    # set and format the ticks
    ax.xaxis.set_major_locator(day)
    ax.xaxis.set_major_formatter(time_fmt)
    ax.grid(True)

    ax.plot(xs, ys)

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()

    ax.set_ylabel('liczba tweetów na godzine')
    ax.set_title('Liczba wszystkich tweetów zebranych między 05-10 a 22-10-2018.')
    fig.suptitle('Całe dane.', fontsize=16)
    fig.set_size_inches(15, 8)

    # save and quit
    figpath = os.path.join(PLOTS_DIR, 'overall-tweets.png')
    fig.savefig(figpath)
    plt.close(fig)
    print("Overall tweets plot created!")


def debate_all():
    """
    Function producing plot of overall tweets posted during Warsaw debate.
    :return: None
    """
    sql = ("""
            SELECT E.t, E.c
            FROM (
                  SELECT  date_trunc('minute', created_at) as t, count(1) as c
                  FROM tweet
                  GROUP BY t
                  ) as E
            WHERE E.t>'2018-10-12 12:00:00' and E.t<'2018-10-13 00:00:00';
            """)

    xs, ys = get_data(sql)

    # create figure/plot
    fig, ax = plt.subplots()

    # configure tickers
    hour = mdates.HourLocator()  # every hour
    time_fmt = mdates.DateFormatter('%H:%M:%S')

    # set and format the ticks
    ax.xaxis.set_major_locator(hour)
    ax.xaxis.set_major_formatter(time_fmt)
    ax.grid(True)

    ax.plot(xs, ys)

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()

    ax.set_ylabel('liczba tweetów na minute')
    ax.set_title('Liczba wszystkich tweetów w dniu 12-10-2018 między 12:00 a 24:00.')
    fig.suptitle('Dzień debaty.', fontsize=16)
    fig.set_size_inches(20, 10)

    # save and quit
    figpath = os.path.join(PLOTS_DIR, 'debate-all.png')
    fig.savefig(figpath)
    plt.close(fig)
    print("Debate overall tweets plot created!")


def debate_hash():
    """
    Function producing plot of tweets containing #debataWarszawska tag during
    Warsaw debate.
    :return:
    """
    sql = ("""
        SELECT E.t, E.c
        FROM (
              SELECT  date_trunc('minute', created_at) as t, count(1) as c
              FROM (
                    SELECT tweet_id
                    FROM hashtag
                    WHERE lower(tag) like 'debatawarszawska'
                    ) as subtable,
                    tweet
              WHERE tweet.id=subtable.tweet_id
              GROUP BY t
              ) as E
        WHERE E.t>'2018-10-12 12:00:00' and E.t<'2018-10-13 00:00:00';
        """)

    xs, ys = get_data(sql)

    # create figure/plot
    fig, ax = plt.subplots()

    # configure tickers
    hour = mdates.HourLocator()   # every hour
    time_fmt = mdates.DateFormatter('%H:%M:%S')

    # set and format the ticks
    ax.xaxis.set_major_locator(hour)
    ax.xaxis.set_major_formatter(time_fmt)
    ax.grid(True)

    ax.plot(xs, ys)

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()

    ax.set_ylabel('liczba tweetów na minute')
    ax.set_title('Liczba tweetów z #debataWarszawska w dniu 12-10-2018 między 12:00 a 24:00.')
    fig.suptitle('Dzień debaty.', fontsize=16)
    fig.set_size_inches(20, 10)

    # save and quit
    figpath = os.path.join(PLOTS_DIR, 'debate-hash.png')
    fig.savefig(figpath)
    plt.close(fig)
    print("Debate hashtag tweets plot created.")


def debate_users():
    """
    Function producing plot tweeting accounts during debate that tweeted more
    than 100 times.
    :return: None
    """
    sql = """
        SELECT screen_name, E.cid
        FROM (
            SELECT user_id, count(user_id) as cid
            FROM tweet
            WHERE 
                created_at > '2018-10-12 17:00:00' 
                and created_at < '2018-10-12 23:00:00'
            GROUP BY user_id
            ) as E,
            newest_users
        WHERE E.user_id=id and E.cid >= 100
        ORDER BY E.cid DESC
        LIMIT 10;
    """

    people, ys = get_data(sql)

    # create figure/plot
    plt.rcdefaults()
    fig, ax = plt.subplots()

    # Example data
    y_pos = np.arange(len(people))
    # colors = ['orange', 'orange', 'orange', 'orange', 'peachpuff', 'orange',
    #           'deepskyblue', 'orange', 'deepskyblue', 'peachpuff'
    #           ]
    colors = [
        KO_COLOR, KO_COLOR, KO_COLOR, KO_COLOR, KO_COLOR_SUPP, KO_COLOR,
        PIS_COLOR_SUPP, KO_COLOR, PIS_COLOR_SUPP, PIS_COLOR_SUPP
    ]
    ax.barh(y_pos, ys, align='center', color=colors)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(people)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Liczba tweetów/retweetów')
    ax.set_title('10 najczęsciej tweetujących kont podczas debaty (17:00-23:00).')
    fig.set_size_inches(15, 5)

    # save and quit
    figpath = os.path.join(PLOTS_DIR, 'debate-users.png')
    fig.savefig(figpath)
    plt.close(fig)
    print("Debate users plot created.")


def split_tweets():
    """
    Function generating plot that shows number of tweets posted about Jaki or
    Trzaskowski during campaign.
    :return: None
    """
    sql_jaki = """
        SELECT  date_trunc('hour', created_at) as t, count(1) as c
        FROM
            (SELECT tweet_id
            FROM jaki_tweets) as E,
            tweet
        WHERE E.tweet_id=id and created_at > '2018-10-05 00:00:00'
        GROUP BY t;
    """

    sql_trzaskowski = """
        SELECT  date_trunc('hour', created_at) as t, count(1) as c
        FROM
            (SELECT tweet_id
            FROM trzaskowski_tweets) as E,
            tweet
        WHERE E.tweet_id=id and created_at > '2018-10-05 00:00:00'
        GROUP BY t;
    """

    # get data
    j_xs, j_ys = get_data(sql_jaki)
    t_xs, t_ys = get_data(sql_trzaskowski)

    # create figure/plot
    fig, ax = plt.subplots()

    # configure tickers
    day = mdates.DayLocator()  # every day
    time_fmt = mdates.DateFormatter('%d-%m-%Y')

    # set and format the ticks
    ax.xaxis.set_major_locator(day)
    ax.xaxis.set_major_formatter(time_fmt)
    ax.grid(True)

    ax.plot(j_xs, j_ys, color='blue', label='Jaki')
    ax.plot(t_xs, t_ys, color='orange', label='Trzaskowski')

    ax.legend(['Patryk Jaki', 'Rafał Trzaskowski'], loc=2)

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()

    ax.set_ylabel('liczba tweetów na godzine')
    ax.set_title('Liczba wszystkich tweetów zebranych między 05-10 a 22-10-2018.')
    fig.suptitle('Całe dane związane z kandydatami.', fontsize=16)
    fig.set_size_inches(15, 8)

    # save and quit
    figpath = os.path.join(PLOTS_DIR, 'overall-tweets-candidates.png')
    fig.savefig(figpath)
    plt.close(fig)
    print("Overall candidates tweets plot created!")


def most_tweets():
    """
    Function generating plot of users with most tweets overall.
    :return: None
    """
    sql = """
        SELECT screen_name, count(E.user_id) as cuid
        FROM
            (SELECT DISTINCT id, user_id, count(id) AS cid 
            FROM tweet 
            GROUP BY id, user_id 
            ORDER BY cid DESC) as E,
            newest_users
        WHERE newest_users.id=E.user_id
        GROUP BY E.user_id, screen_name
        ORDER BY cuid DESC
        LIMIT 15;
    """

    # get data
    people, ys = get_data(sql)

    # create plot/figure
    plt.rcdefaults()
    fig, ax = plt.subplots()

    y_pos = np.arange(len(people))

    # colors = ['deepskyblue', 'orange', ]
    colors = [
        PIS_COLOR_SUPP, KO_COLOR, PIS_COLOR_SUPP, PIS_COLOR_SUPP, KO_COLOR_SUPP,
        KO_COLOR, PIS_COLOR_SUPP, PIS_COLOR_SUPP, PIS_COLOR_SUSP, KO_COLOR_SUPP,
        JOURNALIST_COLOR, KO_COLOR_SUPP, KO_DELETED_COLOR, KO_COLOR, PIS_COLOR_SUSP
    ]
    ax.barh(y_pos, ys, align='center', color=colors)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(people)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Liczba tweetów/retweetów')
    ax.set_title('15 najczęsciej tweetujących kont.')
    fig.set_size_inches(20, 10)

    # save and quit
    figpath = os.path.join(PLOTS_DIR, 'overall-users.png')
    fig.savefig(figpath)
    plt.close(fig)
    print("Most tweeting users overall plot created.")


if __name__ == '__main__':
    # get_all_tweets()
    # debate_all()
    # debate_hash()
    # debate_users()
    # split_tweets()
    most_tweets()
    pass
