"""
Modul sciaga liczbe followersow kandydatow.
"""

import tweepy
import os
import datetime

import config

RESULT_PATH = "candidates"

auth = tweepy.OAuthHandler(config.cost_key, config.cost_skey)
auth.set_access_token(config.acc_key, config.acc_skey)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


cities = {
	"Wwa" : 
		[
			("Trzaskowski", "trzaskowski_"),
			("Jaki", "PatrykJaki")
		]
}


# make directories for elections
for city in cities:
	path = os.path.join(RESULT_PATH, city)
	os.makedirs(path, exist_ok=True)


# get info of each candidate
for city in cities:
	for candidate, tt_account in cities[city]:
		user = api.get_user(tt_account)
		time = datetime.datetime.now()
		followers = user.followers_count
		path = os.path.join(RESULT_PATH, city, "followees")
		result = candidate + "," + str(time) + "," + str(followers)
		with open(path, 'a') as f:
			f.write(result + '\n')