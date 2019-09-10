# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
Module taking care of analysis classified bots.
"""
from config import DB_CONNECTION
# from config import PLOTS_DIR

import string
import numpy as np
import texttable as tt
import psycopg2
import nltk
# make sure that nltk packages are downloaded
nltk.download('punkt')
nltk.download('stopwords')

ACTIVE_FILE = 'activeness.txt'
OLD_ACTIVE_FILE = 'old_activeness.txt'

# Consumer API keys
# (API key)
cost_key = "DOTBsyRQFv1jTPJ3jcxLlpmpH"

# (API secret key)
cost_skey = "uVaLJsq8KxdiSMvuhvnq3uEA87goeURyqa0lTVdp2ixPAbYbqh"

# Access token & access token secret
# (Access token)
acc_key = "883066347172835331-WUWL761WQer3t8si3RkAZrLkLwpGcYK"

# (Access token secret)
acc_skey = "hjwUaTdcnPoBGWDv5KAhMXpSVa06R6IKIEKz8ad9JsjPP"


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
        # xs = []
        # ys = []
        result = []
        # print(len(data))
        for t in data:
            row = [f for f in t]
            # print(len(t))
            # print(row)
            # exit()
            # xs.append((t[0]))
            # ys.append(t[1])
            result.append(row)
        cur.close()
        # return xs, ys
        return result
    except Exception as e:
        print("I am unable to connect to the database, due to\n")
        print(e)
        exit()


def create_sql_ids(bots):
    """
    Function producing part of SQL query of where clause limiting to given ids.
    :param bots: List of bots ids.
    :return: Part of SQL query = "id IN (list of ids)".
    """
    sql = "IN ("
    # concatenate ids
    for bot in bots:
        sql += str(bot) + ", "
    # eliminate trailing comma and space
    # terminate clause
    sql = sql[:-2] + ')'
    return sql

def count_bot_tweets(bots):
    """
    Function counting tweets of bots.
    :param bots: Numpy array with bots (id, name, date of creation).
    :return:
    """
    with open(OLD_ACTIVE_FILE, 'w') as f:
        print("Bots count {}.".format(len(bots)), file=f)
    print("Bots count {}.".format(len(bots)))

    # get ids
    sql_where = create_sql_ids(bots[:, 0])

    sql = """
            SELECT SUM(E2.count)
            FROM
                (
                    SELECT user_id, count(user_id) as count
                    FROM newest_tweets
                    WHERE user_id {}
                    GROUP BY user_id
                ) as E2;
        """.format(sql_where, sql_where)

    res = get_data(sql)
    print(res)



def check_old_activness(bots):
    """
    Function checking activness of bots.
    :param bots: Numpy array with bots (id, name, date of creation).
    :return:
    """
    with open(OLD_ACTIVE_FILE, 'w') as f:
        print("Bots count {}.".format(len(bots)), file=f)
    print("Bots count {}.".format(len(bots)))

    # get ids
    sql_where = create_sql_ids(bots[:, 0])

    sql = """
        SELECT E.screen_name, E.created_at, E2.count, E.statuses_count, E.followers_count,
            E.friends_count, E.favourites_count, E.listed_count
        FROM
            (
                SELECT *
                FROM oldest_users
                WHERE id {}
            ) as E,
            (
                SELECT user_id, count(user_id) as count
                FROM newest_tweets
                WHERE user_id {}
                GROUP BY user_id
            ) as E2
        WHERE E.id=E2.user_id
        ORDER BY E2.count DESC
        LIMIT 20;
    """.format(sql_where, sql_where)

    res = get_data(sql)
    tab = tt.Texttable()
    headers = [
        'Name', 'Created_at', 'Tweets', 'Statuses',
        'Followers', 'Friends', 'Favourites', 'Listed'
    ]
    tab.header(headers)
    tab.set_cols_width([15, 19, 7, 8, 9, 7, 10, 7])
    with open(OLD_ACTIVE_FILE, 'a') as f:
        for row in res:
            print(row, file=f)
            tab.add_row(row)
    s = tab.draw()
    with open(OLD_ACTIVE_FILE+'.table', 'w') as f:
        print(s, file=f)


def check_activness(bots):
    """
    Function checking activness of bots.
    :param bots: Numpy array with bots (id, name, date of creation).
    :return:
    """
    with open(ACTIVE_FILE, 'w') as f:
        print("Bots count {}.".format(len(bots)), file=f)
    print("Bots count {}.".format(len(bots)))

    # get ids
    sql_where = create_sql_ids(bots[:, 0])

    sql = """
        SELECT E.screen_name, E.created_at, E2.count, E.statuses_count, E.followers_count,
            E.friends_count, E.favourites_count, E.listed_count
        FROM
            (
                SELECT *
                FROM newest_users
                WHERE id {}
            ) as E,
            (
                SELECT user_id, count(user_id) as count
                FROM newest_tweets
                WHERE user_id {}
                GROUP BY user_id
            ) as E2
        WHERE E.id=E2.user_id
        ORDER BY E2.count DESC
        LIMIT 20;
    """.format(sql_where, sql_where)

    res = get_data(sql)
    tab = tt.Texttable()
    headers = [
        'Name', 'Created_at', 'Tweets', 'Statuses',
        'Followers', 'Friends', 'Favourites', 'Listed'
    ]
    tab.header(headers)
    tab.set_cols_width([15, 19, 7, 8, 9, 7, 10, 7])
    with open(ACTIVE_FILE, 'a') as f:
        for row in res:
            print(row, file=f)
            tab.add_row(row)
    s = tab.draw()
    with open(ACTIVE_FILE+'.table', 'w') as f:
        print(s, file=f)


def lemmatize(text):
    """
    Lemmatizer of text to list of words in primitive form.
    It does:
    - lowering the letters
    - removing punctation signs
    - tokenizing into polish words
    - removing polish and english stopwords
    :param text: String to lemmatize.
    :return: Lemmatized list of words.
    """
    # to lower case all the letters
    desc = text.lower()
    # delete punctation
    desc.maketrans('', '', string.punctuation)
    # tokenize to polish words
    desc = nltk.word_tokenize(desc, language="polish")

    # eliminate rest of punctations
    desc = [word for word in desc if word.isalpha()]

    # delete stopwords polish and english
    pol_sw = nltk.corpus.stopwords.words('polish')
    eng_sw = nltk.corpus.stopwords.words('english')
    desc = [word for word in desc if not ((word in pol_sw) or (word in eng_sw))]

    return desc


def text_token_counter(sql, outfile):
    """
    Method getting descriptions of users and counting token appearing in them.
    :param sql: SQL getting descriptions
    :param outfile: Path to output file.
    :return:
    """
    print('Handling {}'.format(outfile))
    res = get_data(sql)
    count_all_tts = 0

    words = {}

    # go through descriptions
    for r in res:
        count_all_tts += 1
        # lemmatize and transform words excluding punctation etc
        desc = lemmatize(r[0])
        # go through tokens in dsc
        for wl in desc:
            ac = words.get(wl, 0)
            words[wl] = ac + 1

    # sort them and output
    words_sorted = sorted(words.items(), key=lambda x: x[1], reverse=True)
    # create table
    tab = tt.Texttable()
    headers = ['token', 'count']
    tab.header(headers)
    # tab.set_cols_width([15, 19, 7, 8, 9, 7, 10, 7])
    for v in words_sorted[:25]:
        tab.add_row(v)
    s = tab.draw()
    with open(outfile, 'w') as f:
        print(s, file=f)
        print(count_all_tts, file=f)


def get_dsc_bots(bots):
    """
    Method getting counts of token existing in bots profiles descriptions.
    :param bots: List of bots.
    :return:
    """
    sql_where = create_sql_ids(bots[:, 0])

    sql = """
        SELECT DISTINCT ON (id) description
        FROM twitter_user_dsc
        WHERE id {};
        """.format(sql_where)

    outfile = 'tokens_dsc_bots.txt'
    return text_token_counter(sql, outfile)


def get_dsc_all():
    """
    Method getting counts of token existing in all the profiles descriptions.
    :return:
    """
    sql = """
    SELECT DISTINCT ON (id) description
    FROM twitter_user_dsc;
    """

    outfile = 'tokens_dsc_all.txt'
    return text_token_counter(sql, outfile)


def get_tweet_tokens_all():
    """
    Method getting counts of tokens existing in the tweets made by users.
    :return:
    """
    sql = """
    SELECT tweet
    FROM newest_tweets;
    """

    outfile = 'tokens_tweet_all.txt'
    return text_token_counter(sql, outfile)


def get_tweet_tokens_bots(bots):
    """
    Method getting counts of tokens existing in the tweets made by bots.
    :param bots: List of bots.
    :return:
    """
    sql_where = create_sql_ids(bots[:, 0])

    sql = """
    SELECT tweet
    FROM newest_tweets
    WHERE user_id {};
    """.format(sql_where)

    outfile = 'tokens_tweet_bots.txt'
    return text_token_counter(sql, outfile)


def load_bots_data(filename):
    """
    Method returning uploaded bots data.
    :param filename: Path to file
    :return:
    """
    bots = []
    # read file
    with open(filename, 'r') as f:
        lines = f.readlines()
        # read line of bot entry
        for line in lines:
            line = line.strip().split(' ')
            # get bot id, name and date of creation
            bot_id = line[0][1:]
            bot_date = line[1]
            bot_name = line[3][:-1]
            bots.append((bot_id, bot_name, bot_date))

    # transform to numpy array
    bots = np.asarray(bots)
    return bots


# BOTS_FILE = 'fajneBoty.txt'
BOTS_FILE = 'boty.txt'

if __name__ == '__main__':

    new_bots = load_bots_data(BOTS_FILE)

    count_bot_tweets(new_bots)
    check_old_activness(new_bots)
    check_activness(new_bots)

    get_tweet_tokens_all()
    get_tweet_tokens_bots(new_bots)
    get_dsc_bots(new_bots)
    get_dsc_all()
