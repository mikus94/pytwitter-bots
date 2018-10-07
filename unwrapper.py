#-*- coding: utf-8 -*-
import time

def parse_time(time_str):
	"""
	Parsing twitter time to python time.
	"""
	ts = time.strftime(
		'%Y-%m-%d %H:%M:%S', 
		time.strptime(
			time_str,
			'%a %b %d %H:%M:%S +0000 %Y'
		)
	)
	return ts

def get_tweet(json):
	"""
	Getting exact tweet.

	Returns:
	
	(*)quote
	quoting_user, ????
	
	(*)retweet
	retweeting_user, retweeted_tweet_id
	
	(*)tweet
	user, tweet
	"""
	# check whetver tweet is tweet, retweet or quote tweet.
	user = get_user(json)
	tweet = get_tweet_data(json)
	# retweet
	if (json.get('retweeted_status', None) != None):
		print("Retweet!")
		# get retweeted tweet data
		retweeted = get_tweet_data(json.get('retweeted_status', {}))
		date = parse_time(json.get('created_at', None))
		retweet = {
			'id'		: tweet['id'],
			'tweet_id' 	: retweeted['id'],
			'user_id'		: user['id'],
			'created_at': date
		}
		return ('retweet', (user, tweet, retweet))
	# quoted
	elif (json.get('is_quote_status', False) == True):
		print("Quote!")
		quoted_tweet = get_tweet_data(json.get('quoted_status', {}))
		quoted = {
			'id' 		: tweet['id'],
			'quoted' 	: quoted_tweet
		}
		return ('quote', (user, tweet, quoted))
	# regular tweet
	else:
		print("Tweet!")
		return ('tweet', (user, tweet))

def get_tweet_data(json):
	"""
	Get regular tweet data.
	"""
	tweet = {}
	tweet['id'] = int(json['id_str'])
	tweet['user_id'] = int(json['user']['id_str'])

	tweet['retweeted'] = False

	tweet['created_at'] = parse_time(json['created_at'])
	tweet['tweet'] = json.get('full_text', '')
	tweet['lang'] = json.get('lang', '')
	if json.get('place', None) != None:
		tweet['place'] = json['place'].get('full_name', '')
	else:
		tweet['place'] = ''

	tweet['retweet_count'] = json.get('retweet_count', 0)
	tweet['favourites_count'] = json.get('favourites_count', 0)

	tweet['entities'] = get_entities(json['entities'])

	# check if any additional media was attached 
	# ('native' media uploaded to twitter)
	extended = json.get('extended_entities', None)
	if extended != None:
		extended_media = [ (em['type'], em['media_url']) for em in extended.get('media', {}) ]
		tweet['entities']['media'] = extended_media
	return tweet

def get_entities(json):
	"""
	Getting entities like hashtags and user mentions
	"""
	# get all hashtags appearing in tweet
	hashtags = json['hashtags']
	hashtags = [ h['text'] for h in hashtags ]
	# get all urls
	urls = [ u['expanded_url'] for u in json.get('urls', {}) ]
	# get all mentions
	user_mentions = [ 
		(um['screen_name'], int(um['id_str'])) for um in json.get('user_mentions', {})
	]
	media = [ (m['type'], m['media_url']) for m in json.get('media', {}) ]
	entities = {
		'hashtags' : hashtags,
		'urls' : urls,
		'user_mentions' : user_mentions,
		'media' : media
	}
	return entities




		


def get_user(json):
	"""
	Getting user info out of tweet.
	Extracting information beeing used in following analizys.
	"""
	author_json = json['user']
	author = {}
	# id
	author['id'] = int(author_json['id_str'])
	# created_at
	author['created_at'] = parse_time(author_json['created_at'])
	# lang
	author['lang'] = author_json.get('lang', 'xx')
	# profile attributes
	attributes_to_get = [
		# user name
		'screen_name',
		# profile attributes
		'default_profile',
		'default_profile_image',
		'profile_use_background_image',
		'statuses_count',
		'followers_count',
		'friends_count',
		'favourites_count',
		'listed_count',
		'geo_enabled',
		'verified',
		'protected',
		'description',
		'location'
	]
	for att in attributes_to_get:
		author[att] = author_json.get(att, '')
	# returning json with less data
	return author

