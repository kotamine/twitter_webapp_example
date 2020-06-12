import tweepy as tw
#from local_config import *


if __name__=="__main__":
	consumer_key= 'H8zipXQORIOKTCc9QRTDhWBfP'
	consumer_secret= 'rTPTC3CtsS6Im0KVi52kKpagTVmO9Pd4KKJgN4SweGmsPhXN43'
	access_token= '146167412-JnC2AqQoSx3yw6eaP5MfjjuczFvohz1aWXeS99Pp'
	access_secret= '1gGKNVnKnB7djsU87xCJK9EYf2lD1WZ1o47gQ5W6AYm3J'

	# consumer_key = os.getenv("CONSUMER_KEY")
	# consumer_secret = os.getenv("CONSUMER_SECRET")
	# access_token = os.getenv("ACCESS_TOKEN")
	# access_secret = os.getenv("ACCESS_SECRET")

	auth = tw.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tw.API(auth, 
		wait_on_rate_limit = True, 
		wait_on_rate_limit_notify = True)

	# Search 
	search_results = tw.Cursor(api.search, 
		q = "#BlackLivesMatter").items(100)
	[ print(result.text) for result in search_results ]

	trends = api.trends_place(1)

	[ print(trend["name"]) for trend in trends[0]["trends"] ]
	