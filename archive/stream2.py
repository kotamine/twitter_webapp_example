import tweepy as tw
from myconfig import *
import json

class twitter_listener(tw.StreamListener):

	def __init__(self, num_tweets_to_grab):
		self.counter = 0
		self.num_tweets_to_grab = num_tweets_to_grab


	def on_data(self, data):
		try:
			j = json.loads(data)
			print(j["text"])
			self.counter += 1
			if self.counter == self.num_tweets_to_grab:
				return False
			return True
		except:
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

	listner = twitter_listener(api, num_tweets_to_grab=10)
	twitter_stream = tw.Stream(auth, listner)
	try:
		twitter_stream.sample()
	except Exception as e:
		print(e.__doc__)
		

		
