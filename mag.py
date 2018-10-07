#-*- coding: utf-8 -*-
import tweepy
import json

from storage import DbHandler, StorageHandler

import config
import unwrapper

auth = tweepy.OAuthHandler(config.cost_key, config.cost_skey)
auth.set_access_token(config.acc_key, config.acc_skey)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


db = DbHandler()
storage = StorageHandler()


# exit()


i = 0
tag = '#Trzaskowski'
for tweet in tweepy.Cursor(api.search, q=tag, count=100, \
							since="2018-10-05", tweet_mode='extended').items():
	
	

	i += 1
	storage.save_raw_tweet(tweet._json)
	# unwrap tweet
	(t_type, res) = unwrapper.get_tweet(tweet._json)
	if t_type == 'tweet':
		(user, tweet) = res
		storage.save_user(user)
		storage.save_tweet(tweet)
		db.insert_tweet(tweet)
		db.insert_user(user)
	elif t_type == 'retweet':
		(user, tweet, retweet) = res
		storage.save_user(user)
		storage.save_tweet(tweet)
		storage.save_retweet(retweet)
		db.insert_retweet(retweet)
	elif t_type == 'quote':
		(user, tweet, quoted) = res
		storage.save_user(user)
		storage.save_tweet(tweet)
		storage.save_quoted(quoted)
		db.insert_quoted(quoted)
	else:
		print("ERROR!!!")
db.close()
print("There was " + str(i) + " tweets with " + tag)