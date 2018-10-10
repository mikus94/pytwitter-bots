# -*- coding: utf-8 -*-
"""
Author: Mikolaj Gagatek
Masters Degree Thesis application.
Application downloading tweets using Twitter API.
"""
"""
Module defining storage objects.
"""
import psycopg2
import os
import json
import datetime

# get pwd
PWD = os.path.abspath(os.path.dirname(__file__))
# create paths
DATA_USERS = os.path.join(PWD, 'data/users')
DATA = os.path.join(PWD, 'data/content')
RAW_DATA = os.path.join(PWD, 'data/raw')

TODAY = str(datetime.date.today()) + "@" + str(datetime.datetime.today().time())


class Singleton(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Logger(metaclass=Singleton):
    """
    Class that writes logs about computation into the file. It also prints info
    on standard output.
    """
    def __init__(self):
        """
        Initialization of logger.
        """
        self.log_path = os.path.join(PWD, 'data/logs')
        self.tags_path = os.path.join(PWD, 'data/tags')
        os.makedirs(self.log_path, exist_ok=True)
        os.makedirs(self.tags_path, exist_ok=True)
        self.log_path = os.path.join(self.log_path, TODAY)

    def tag_stats(self, tag, all_tt, tt, rt, qt):
        """
        Log info about downloading given tag.
        :param tag: String containing tag.
        :param tt: Integer determining number tweets containing given tag.
        :param rt: Integer determining number of retweets of tweets with given
            tag.
        "param qt: Integer determining number of quoted tweets containing tag.
        """
        all_tts = "All actions: " + str(all_tt)
        tts = 'Tweets: ' + str(tt)
        rts = 'Retweets: ' + str(rt)
        qts = 'Quoted: ' + str(qt)
        # log to file
        with open(os.path.join(self.tags_path, tag), 'w') as f:
            f.write(tag + '\n')
            f.write(all_tts + '\n')
            f.write(tts + '\n')
            f.write(rts + '\n')
            f.write(qts + '\n')
        # log to stdout
        log = (
            "Tag \'" + tag + "\' info:\n{" + 
            all_tts + ", " + tts + ", " + rts + ", " + qts + "}"
        )
        print(log)
        with open(self.log_path, 'a') as f:
            f.write(log + '\n')

    def tag_start(self, tag):
        """
        Log info about begining of diggig.
        :param tag: String with tag.
        """
        log = "\'" + tag + "\'\n"
        log = log + "Start digging \'" + tag + "\'."
        with open(self.log_path, 'a') as f:
            f.write(log + '\n')
        print(log)

    def tag_finish(self, tag):
        """
        Log info about finished digging.
        :param tag: String with tag.
        """
        log = "Finished digging tag: \'" + tag + "\'."
        with open(self.log_path, 'a') as f:
            f.write(log + '\n\n')
        print(log + '\n')

    def download_info(self, since, until, tags, no_data):
        """
        Logging info about digging process.
        :param since: Date indicating start point of digging tweets.
        :param until: Date indicating end point of digging tweets.
        :param tags: List of tags that were digged.
        :param no_data: Number of tweets digged.
        """
        log = (
            "End of downloading. In total there were " + str(no_data) +
            " tweets downloaded.\n" +
            "These tweets were posted from " + str(since) + " to " +
            str(until) + "."
        )
        print("\n" + log + "\n")
        with open(self.log_path, 'a') as f:
            f.write('==================================' + '\n')
            f.write(log + '\n')
            f.write("Tags downloaded are listed below." + '\n')
            f.write(str(tags) + '\n')
            f.write('==================================' + '\n')



class MultiStorage(metaclass=Singleton):
    """
    Class does both DB and file storage.
    """
    def __init__(self):
        """
        Initialization
        """
        self.db = DbHandler()
        self.files = StorageHandler()

    def save(self, data):
        """
        Saving tweet data passed by JSON containing user, tweet and maybe
        retweet or quoted data.
        :param data: JSON obtained after unwrapping Twitter API JSON.
        """
        self.save_user(data['user'])
        if (data.get('tweet', None) is not None):
            self.save_tweet(data['tweet'])
        if (data.get('retweet', None) is not None):
            self.save_retweet(data['retweet'])
        if (data.get('quoted', None) is not None):
            self.save_quoted(data['quoted'])

    def save_tweet(self, tweet):
        """
        Saving tweets in file system and db.
        :param tweet: My Tweet JSON.
        """
        self.db.insert_tweet(tweet)
        self.files.save_tweet(tweet)

    def save_retweet(self, retweet):
        """
        Saving retweet in file system and db
        :param retweet: My Retweet JSON.
        """
        self.db.insert_retweet(retweet)
        self.files.save_retweet(retweet)

    def save_quoted(self, quoted):
        """
        Saving quote in file system and db.
        :param quoted: My Quoted JSON.
        """
        self.db.insert_quoted(quoted)
        self.files.save_quoted(quoted)

    def save_user(self, user):
        """
        Saving user in file system and db.
        :param user: My User JSON.
        """
        self.db.insert_user(user)
        self.files.save_user(user)

    def save_raw_tweet(self, tweet):
        """
        Saving raw tweet json to file.
        :param tweet: Raw tweet json.
        """
        self.files.save_raw_tweet(tweet)

    def close_db(self):
        """
        Closing db connection.
        """
        self.db.close()


class DbHandler(metaclass=Singleton):
    """
    Class handling database connection and operation inside it.
    """
    def __init__(self):
        """
        Initializer creating connection to database.
        """
        try:
            self.conn = psycopg2.connect(
                """dbname='twitter'
                user='postgres'
                host='localhost'
                password='1234'"""
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            print("I am unable to connect to the database, due to\n")
            print(e)
            exit()

    def execute_sql(self, sql, data):
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

    def create_sql(self, table_name, data):
        """
        Creating SQL query (insert) appropriate to the data and table.
        :param table_name: Name of a table for query.
        :param data: Dict used in query.
        :returns: Full SQL query executing insertion of given data.
        """
        # creation of sql statement
        keys = "INSERT INTO " + table_name + "("
        values = "VALUES ("
        for k in data.keys():
            if k == 'entities':
                continue
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
        sql = self.create_sql('tweet', tweet)
        # execute
        self.execute_sql(sql, tweet)
        # insert entites
        self.insert_entities(tweet)

    def insert_entities(self, tweet):
        """
        Method inserting all of tweets entities.
        :param tweet:
        """
        # mentions
        tweet_id = tweet['id']
        mentions = tweet['entities']['user_mentions']
        if mentions != []:
            # get all mentions
            users = [u[1] for u in mentions]
            # create sql
            sql = ("""INSERT INTO mentions(tweet_id, user_id)
                      VALUES (%(tweet_id)s, %(user_id)s);""")
            # insert all mentions
            for u in users:
                self.execute_sql(sql, {'tweet_id': tweet_id, 'user_id': u})
        # hashtags
        hashtags = tweet['entities']['hashtags']
        if hashtags != []:
            # sql
            sql = ("""INSERT INTO hashtag(tweet_id, tag)
                      VALUES (%(tweet_id)s, %(tag)s);""")
            # insert all
            for h in hashtags:
                self.execute_sql(sql, {'tweet_id': tweet_id, 'tag': h})
        # urls
        urls = tweet['entities']['urls']
        if urls != []:
            # sql
            sql = ("""INSERT INTO urls(tweet_id, link)
                      VALUES (%(tweet_id)s, %(link)s);""")
            for l in urls:
                self.execute_sql(sql, {'tweet_id': tweet_id, 'link': l})
        # media
        media = tweet['entities']['media']
        if media != []:
            # get all media
            m = [(md[0], md[1]) for md in media]
            sql = ("""INSERT INTO media(tweet_id, type, link)
                      VALUES (%(tweet_id)s, %(type)s, %(link)s);""")
            for (t, l) in m:
                self.execute_sql(
                        sql,
                        {
                            'tweet_id': tweet_id,
                            'type': t,
                            'link': l
                        }
                )

    def insert_user(self, user):
        """
        Method insering user into DB.
        """
        sql = self.create_sql('twitter_user', user['user'])
        sql2 = self.create_sql('twitter_user_dsc', user['dsc_info'])
        self.execute_sql(sql, user['user'])
        self.execute_sql(sql2, user['dsc_info'])

    def insert_retweet(self, retweet):
        """
        Method inserting retweets into db.
        """
        sql = self.create_sql('retweets', retweet)
        self.execute_sql(sql, retweet)

    def insert_quoted(self, quoted):
        """
        Method inseting quote.
        """
        # insert quoted tweet.
        self.insert_tweet(quoted['quoted'])
        sql = ("""INSERT INTO quotes(id, quoted_id)
                  VALUES (%(id)s, %(quoted)s)""")
        self.execute_sql(
            sql,
            {
                'id': quoted['id'],
                'quoted': quoted['quoted']['id']
            }
        )

    def close(self):
        self.conn.close()


class StorageHandler(metaclass=Singleton):
    """
    Class handling storing data into the files.
    """

    def __init__(self):
        # create output dirs
        os.makedirs(DATA, exist_ok=True)
        os.makedirs(DATA_USERS, exist_ok=True)
        os.makedirs(RAW_DATA, exist_ok=True)

        self.path_r = os.path.join(DATA, 'retweets')
        self.path_t = os.path.join(DATA, 'tweets')
        self.path_q = os.path.join(DATA, 'quotes')

        os.makedirs(self.path_r, exist_ok=True)
        os.makedirs(self.path_t, exist_ok=True)
        os.makedirs(self.path_q, exist_ok=True)

    def format_json(self, data):
        """
        Formating json to desired output.
        """
        return json.dumps(data, indent=3, ensure_ascii=False)

    def save_json(self, path, filename, data):
        """
        Method printing json to desired file.
        """
        filepath = os.path.join(path, filename)
        with open(filepath, 'w') as f:
            f.write(self.format_json(data))

    def print_json(self, data):
        """
        Printing json to standard output.
        """
        print(self.format_json(data))

    def save_tweet(self, tweet):
        """
        Method saving tweets.
        """
        self.save_json(self.path_t, str(tweet['id']), tweet)

    def save_retweet(self, retweet):
        """
        Method saving retweets.
        """
        self.save_json(self.path_r, str(retweet['id']), retweet)

    def save_quoted(self, quoted):
        """
        Method saving quotes.
        """
        self.save_json(self.path_q, str(quoted['id']), quoted)

    def save_user(self, user):
        """
        Method saving users.
        """
        filename = (user['user']['screen_name'] + '@' + user['user']['version'])
        self.save_json(DATA_USERS, filename, user)

    def save_raw_tweet(self, tweet):
        """
        Saving raw Tweet.
        """
        self.save_json(RAW_DATA, str(tweet['id']), tweet)
