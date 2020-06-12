import tweepy as tw
from myconfig import *
import json
from collections import Counter
import pdb
import sqlite3
import time

# db = "twitter_data.db"
db = "/data/twitter_data.db"


langs = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
         'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
         'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
         'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
         'vi': 'Vietnamese', 'zh_CN': 'Chinese (simplified)', 'zh_TW': 'Chinese (traditional)'}

class TwitterMain():
	def __init__(self, num_tweets_to_grab, retweet_count, conn):

		# keys from myconfig.py
		self.auth = tw.OAuthHandler(consumer_key, consumer_secret)
		self.auth.set_access_token(access_token, access_secret)
		self.api = tw.API(self.auth, 
			wait_on_rate_limit = True, 
			wait_on_rate_limit_notify = True)
		self.num_tweets_to_grab = num_tweets_to_grab
		self.retweet_count = retweet_count
		self.stats = Stats()
		self.conn = conn
		self.c = self.conn.cursor()


	def get_trends(self):
		trends = self.api.trends_place(1)
		trend_data = []
		
		print("\n------ Trends ------:")
		for trend in trends[0]["trends"]:
			# print(trend["name"]) 
			trend_tweets = []
			trend_tweets.append(trend['name'])
			search_results = tw.Cursor(self.api.search, 
				q = trend['name'], #result_type="recent"
				).items(3)
			
			for result in search_results:
				trend_tweets.append(result.text)
				#print(result.text)

			trend_data.append(tuple(trend_tweets))

		print(trend_data)
		try: 
			self.c.executemany("INSERT INTO trend_data VALUES (?,?,?,?, DATETIME('now','localtime'))",
				trend_data)
			self.conn.commit()
			print("trend data added")
		except Exception as e:
			print(e.__doc__)


	def get_streaming_data(self):
		listner = TwitterListener(self.api, self.stats, 
			self.num_tweets_to_grab, self.retweet_count) #self.get_tweet_html,
		twitter_stream = tw.Stream(self.auth, listner)
		
		print("\n------ Streaming -------:")
		try:
			twitter_stream.sample()
		except Exception as e:
			print(e.__doc__)

		lang, top_lang, top_tweets = self.stats.get_stats()
		print(Counter(lang))
		print(Counter(top_lang))
		print(top_tweets)

		self.c.execute("INSERT INTO lang_data VALUES (?,?,DATETIME('now','localtime'))",
			(str(list(Counter(lang).items())), 
			str(list(Counter(top_lang).items()))))
		
		for tweet in top_tweets:
		 	self.c.execute("INSERT INTO twit_data VALUES (?,DATETIME('now','localtime'))",
		 	(tweet,))

		self.conn.commit()



class TwitterListener(tw.StreamListener):

	def __init__(self, api, stats, num_tweets_to_grab,
					 retweet_count=10000): #get_tweet_html,
		self.counter = 0
		self.num_tweets_to_grab = num_tweets_to_grab
		self.retweet_count = retweet_count
		self.languages = []
		self.top_languages = []
		self.stats = stats
		#self.get_tweet_html = []#get_tweet_html

	def on_data(self, data):
		try:
			json_data = json.loads(data)
			#self.languages.append(langs[json_data["lang"]])
			self.stats.add_lang(langs[json_data["lang"]])
			self.counter += 1
			retweet_count = json_data["retweeted_status"]["retweet_count"]

			if retweet_count >= self.retweet_count:
				#print(json_data["text"], retweet_count, json_data["lang"])
				#self.top_languages.append(langs[json_data["lang"]])
				self.stats.add_top_lang(langs[json_data["lang"]])
				if 'retweeted_status' in json_data:
					if 'text' in json_data['retweeted_status']:
						self.stats.add_top_tweets(json_data['retweeted_status']['text'])

			if self.counter >= self.num_tweets_to_grab:
				# print(self.languages)
				# print(Counter(self.languages))
				return False
			
			return True
		except:
			# @TODO: come back to this
			pass

	def on_error(self, status):
		print(status)




class Stats():
	def __init__(self):
		self.lang = []
		self.top_lang = []
		self.top_tweets = []

	def add_lang(self, lang):
		self.lang.append(lang)

	def add_top_lang(self, top_lang):
		self.top_lang.append(top_lang)

	def add_top_tweets(self, tweet_html):
		self.top_tweets.append(tweet_html)

	def get_stats(self):
		return self.lang, self.top_lang, self.top_tweets



if __name__=="__main__":
	counter = 1
	num_tweets_to_grab = 1000 # num of sampling gathered in streaming API  
	retweet_count = 10000 # defition of 'top tweets' with many retweets

	try: 
		while True: # run continuously until stopped
			print('\n---------------------- counter: ', counter, 
				'-------------------------')
			conn = sqlite3.connect(db)
			twit = TwitterMain(num_tweets_to_grab, retweet_count, conn)
			twit.get_streaming_data()
			if counter==1:
				twit.get_trends()				
			counter = counter +1

			time.sleep(5) # 5 seconds of sleep 
			if counter%60==0: # every 60th time update trends
				twit.get_trends() 
		
	except Exception as e:
		print(e.__doc__)

	finally:
		conn.close()



		
