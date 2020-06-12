import tweepy as tw
from myconfig import *
import json
from collections import Counter
import pdb


langs = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
         'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
         'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
         'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
         'vi': 'Vietnamese', 'zh_CN': 'Chinese (simplified)', 'zh_TW': 'Chinese (traditional)'}

class TwitterMain():
	def __init__(self, api):


class twitter_listener(tw.StreamListener):

	def __init__(self, api, num_tweets_to_grab, retweet_count=10000): 
		self.counter = 0
		self.num_tweets_to_grab = num_tweets_to_grab
		self.retweet_count = retweet_count
		self.languages = []
		self.top_languages = []

	def on_data(self, data):
		try:
			json_data = json.loads(data)
			self.languages.append(langs[json_data["lang"]])
			self.counter += 1
			retweet_count = json_data["retweeted_status"]["retweet_count"]

			if retweet_count >= self.retweet_count:
				print(json_data["text"], retweet_count, json_data["lang"])
				self.top_languages.append(langs[json_data["lang"]])

			if self.counter >= 10:#self.num_tweets_to_grab:
				print(self.languages)
				print(Counter(self.languages))
				return False
			
			return True
		except:
			# @TODO: come back to this
			pass

	def on_error(self, status):
		print(status)

if __name__=="__main__":

	# keys from myconfig.py
	auth = tw.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tw.API(auth, 
		wait_on_rate_limit = True, 
		wait_on_rate_limit_notify = True)

	# Search 
	search_results = tw.Cursor(api.search, 
		q = "#BlackLivesMatter").items(10)
	print("\n ------ Search results ------:")
	[ print(result.text) for result in search_results ]

	trends = api.trends_place(1)

	print("\n ------ Trends ------:")
	[ print(trend["name"]) for trend in trends[0]["trends"] ]
	
	# Stream
	listner = twitter_listener(api, num_tweets_to_grab=1000)
	twitter_stream = tw.Stream(auth, listner)
	print("\n ------ Streaming -------:")
	try:
		twitter_stream.sample()
	except Exception as e:
		print(e.__doc__)
		

		
