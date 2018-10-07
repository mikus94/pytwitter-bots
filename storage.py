#-*- coding: utf-8 -*-
import psycopg2
import os
import json

# get pwd
PWD = os.path.abspath(os.path.dirname(__file__))
# create paths
DATA_USERS = os.path.join(PWD, 'data/users')
DATA = os.path.join(PWD, 'data/content')
RAW_DATA = os.path.join(PWD, 'data/raw')

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
                "dbname='twitter' user='postgres' host='localhost' password='1234'"
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            print("I am unable to connect to the database, due to\n")
            print(e)
            exit()

    def execute_sql(self, sql, data):
        try:
            self.cur.execute(sql, data)
            self.conn.commit()
        except psycopg2.IntegrityError:
            self.conn.rollback()
        except Exception as e:
            print(sql)
            print("Insertion failed due to")
            print(e)
            print(data)
            exit()

    def create_sql(self, table_name, data):
        # creation of sql statement
        keys = "INSERT INTO " + table_name + "("
        values = "VALUES ("
        for k in data.keys():
            if k == 'entities':
                continue
            keys += k + ", "
            values += "%(" + k + ")s, "
        keys = keys[:-2] + ")"
        values = values[:-2] + ");"

        sql = keys + " " + values
        return sql

    def insert_tweet(self, tweet):
        """
        Method inserting tweet into DB.
        """
        sql = self.create_sql('tweet', tweet)
        # execute
        self.execute_sql(sql, tweet)
        # insert entites
        self.insert_entities(tweet)

    def insert_entities(self, tweet):
        """
        Method inserting tweet entities.
        """

        # mentions
        tweet_id = tweet['id']
        mentions = tweet['entities']['user_mentions']
        if mentions != []:
            # get all mentions
            users = [ u[1] for u in mentions ]
            # create sql
            sql = ("""INSERT INTO mentions(tweet_id, user_id) 
                      VALUES (%(tweet_id)s, %(user_id)s);""")
            # insert all mentions
            for u in users:
                self.execute_sql(sql, {'tweet_id' : tweet_id, 'user_id' : u})
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
                self.execute_sql(sql, {'tweet_id': tweet_id, 'link' : l})
        # media
        media = tweet['entities']['media']
        if media != []:
            # get all media
            m = [ (md[0], md[1]) for md in media ]
            sql = ("""INSERT INTO media(tweet_id, type, link) 
                      VALUES (%(tweet_id)s, %(type)s, %(link)s);""")
            for (t, l) in m:
                self.execute_sql(
                        sql, 
                        {
                            'tweet_id' : tweet_id, 
                            'type' : t,
                            'link' : l
                        }
                )


    def insert_user(self, user):
        """
        Method insering user into DB.
        """
        sql = self.create_sql('twitter_user', user)
        self.execute_sql(sql, user)

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
                'id' : quoted['id'], 
                'quoted' : quoted['quoted']['id']
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
        self.save_json(DATA_USERS, user['screen_name'], user)

    def save_raw_tweet(self, tweet):
        """
        Saving raw Tweet.
        """
        self.save_json(RAW_DATA, str(tweet['id']), tweet)
