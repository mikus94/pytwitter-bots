#-*- coding: utf-8 -*-
import tweepy
import json
import os

import config
import unwrapper

auth = tweepy.OAuthHandler(config.cost_key, config.cost_skey)
auth.set_access_token(config.acc_key, config.acc_skey)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


# create output dirs
DATA_USERS = '/home/miko/msc/data/users'
DATA_TAGS = '/home/miko/msc/data/tags'

os.makedirs(DATA_USERS, exist_ok=True)
os.makedirs(DATA_TAGS, exist_ok=True)

def print_json(path, filename, data):
	"""
	Method printing json to desired file.
	"""
	filepath = os.path.join(path, filename)
	with open(filepath, 'w') as f:
		f.write(json.dumps(data, indent=3, ensure_ascii=False))


i = 0
tag = '#Trzaskowski'
for tweet in tweepy.Cursor(api.search, q=tag, count=100, \
							since="2018-10-05", tweet_mode='extended').items():
	
	path = os.path.join(DATA_TAGS, tag)
	path_r = os.path.join(path, 'retweets')
	path_t = os.path.join(path, 'tweets')
	path_q = os.path.join(path, 'quotes')
	
	os.makedirs(path_r, exist_ok=True)
	os.makedirs(path_t, exist_ok=True)
	os.makedirs(path_q, exist_ok=True)

	# unwrap tweet
	(t_type, res) = unwrapper.get_tweet(tweet._json)
	i += 1
	if t_type == 'tweet':
		(user, tweet) = res
		print_json(DATA_USERS, user['screen_name'], user)
		print_json(path_t, str(tweet['id']), tweet)
	elif t_type == 'retweet':
		(user, retweet) = res
		print_json(DATA_USERS, user['screen_name'], user)
		print_json(path_r, str(retweet['id']), retweet)
	elif t_type == 'quote':
		(user, tweet, quoted) = res
		print_json(DATA_USERS, user['screen_name'], user)
		print_json(path_t, str(tweet['id']), tweet)
		print_json(path_q, str(quoted['id']), quoted)
	else:
		print("ERROR!!!")
print("There was " + str(i) + " tweets with " + tag)