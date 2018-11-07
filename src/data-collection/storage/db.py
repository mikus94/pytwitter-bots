# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
"""
import psycopg2
import os
import json
import datetime

from .singleton import Singleton
from configs.data_config import *
from configs.db_config import *

class DbHandler(metaclass=Singleton):
    """
    Class handling database connection and operation inside it.
    """
    def __init__(self):
        """
        Initializer creating connection to database.
        """
        try:
            self.conn = psycopg2.connect(DB_CONNECTION)
            # self.conn = psycopg2.connect(DB_TEST)
            self.cur = self.conn.cursor()
        except Exception as e:
            print("I am unable to connect to the database, due to\n")
            print(e)
            exit()

    def execute_insert(self, sql, data):
        """
        Method executing SQL.
        :param sql: SQL query (insertion) that is passed to DB.
        :param data: Data used to query.
        """
        try:
            # execute sql.
            self.cur.execute(sql, data)
            self.conn.commit()
        except psycopg2.IntegrityError:
            # exception of duplicate insertion.
            # it is ommited beceause of multiple user and tweet appearance.
            # e.g. user posts 2 tweets or tweet is retweeted twice.
            self.conn.rollback()
        except Exception as e:
            # insertion fails.
            print(sql)
            print("Insertion failed due to")
            print(e)
            print(data)
            exit()

    def execute_select(self, sql):
        """
        Method executing SQL select.
        :param sql: Sql with select query.
        :returns list: List of resulting query.
        """
        self.cur.execute(sql)
        # return all the results
        return self.cur.fetchall()


    def create_insert_sql(self, table_name, fields):
        """
        Creates a insertion query to DB.
        :param table_name: Name of table for query.
        :param fields: List of fields in table (with default values).
        :returns: Full sql insertion query for desired table.
        """
        keys = "INSERT INTO " + table_name + "("
        values = "VALUES ("
        for (k,_d,_f) in fields:
            keys += k + ", "
            values += "%(" + k + ")s, "
        # eliminate trailing ", "
        keys = keys[:-2] + ")"
        values = values[:-2] + ");"
        sql = keys + " " + values
        return sql

    def insert_tweet(self, tweet):
        """
        Method inserting tweet with its entities into DB.
        :param tweet: My Tweet JSON.
        """
        sql = self.create_insert_sql(TT_TABLE, TT_FIELDS)
        # execute
        self.execute_insert(sql, tweet)
        # insert entites
        self.insert_entities(tweet)

    def insert_entities(self, tweet):
        """
        Method inserting all of tweets entities.
        :param tweet:
        """
        tweet_id = tweet['id']
        def mentions():
            # mentions
            mentions = tweet['entities']['user_mentions']
            if mentions != []:
                # get all mentions
                users = [u[1] for u in mentions]
                # create sql
                sql = self.create_insert_sql(MENTIONS_TABLE, MENTIONS_FIELDS)
                # insert all mentions
                for u in users:
                    self.execute_insert(sql, {'tweet_id': tweet_id, 'user_id': u})

        def hashtags():
            # hashtags
            hashtags = tweet['entities']['hashtags']
            if hashtags != []:
                # sql
                sql = self.create_insert_sql(HASH_TABLE, HASH_FIELDS)
                # insert all
                for h in hashtags:
                    self.execute_insert(sql, {'tweet_id': tweet_id, 'tag': h})
        
        def urls():
            # urls
            urls = tweet['entities']['urls']
            if urls != []:
                # sql
                sql = self.create_insert_sql(URLS_TABLE, URLS_FIELDS)
                for l in urls:
                    self.execute_insert(sql, {'tweet_id': tweet_id, 'link': l})
        
        def media():
            # media
            media = tweet['entities']['media']
            if media != []:
                # get all media
                m = [(md[0], md[1]) for md in media]
                # sql = ("""INSERT INTO media(tweet_id, type, link)
                #          VALUES (%(tweet_id)s, %(type)s, %(link)s);""")
                sql = self.create_insert_sql(MEDIA_TABLE, MEDIA_FIELDS)
                for (t, l) in m:
                    self.execute_insert(
                            sql,
                            {
                                'tweet_id': tweet_id,
                                'type': t,
                                'link': l
                            }
                    )
        # insert entities body
        mentions()
        hashtags()
        urls()
        media()

    def insert_user(self, user):
        """
        Method insering user into DB.
        """
        sql = self.create_insert_sql(USR_TABLE, USR_FIELDS)
        sql2 = self.create_insert_sql(USR_DSC_TABLE, USR_DSC_FIELDS)
        self.execute_insert(sql, user['user'])
        self.execute_insert(sql2, user['dsc_info'])

    def insert_my_retweet(self, retweet):
        """
        Method inserting retweets into db.
        """
        sql = self.create_insert_sql(RTT_TABLE, RTT_FIELDS)
        self.execute_insert(sql, retweet)

    def insert_my_quoted(self, quoted):
        """
        Method inseting quote.
        """
        # sql
        sql = self.create_insert_sql(QTT_TABLE, QTT_FIELDS)
        self.execute_insert(
            sql,
            {
                'id': quoted['id'],
                'quoted_id': quoted['quoted_id']
            }
        )

    def close(self):
        self.conn.close()