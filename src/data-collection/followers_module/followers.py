"""
Modul sciaga liczbe followersow kandydatow.
"""

import tweepy
import os
import datetime



#Consumer API keys
#(API key)
cost_key = "DOTBsyRQFv1jTPJ3jcxLlpmpH"

#(API secret key)
cost_skey = "uVaLJsq8KxdiSMvuhvnq3uEA87goeURyqa0lTVdp2ixPAbYbqh"

# Access token & access token secret
# (Access token)
acc_key = "883066347172835331-WUWL761WQer3t8si3RkAZrLkLwpGcYK"

 # (Access token secret)
acc_skey = "hjwUaTdcnPoBGWDv5KAhMXpSVa06R6IKIEKz8ad9JsjPP"

RESULT_PATH = "candidates"

auth = tweepy.OAuthHandler(cost_key, cost_skey)
auth.set_access_token(acc_key, acc_skey)

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