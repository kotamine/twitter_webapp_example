from flask import Flask, render_template, jsonify
import sqlite3
import ast

db = "twitter_data.db"

app = Flask(__name__)

@app.route("/")
def main():
	language_data = []
	top_language_data = []
	lang, top_lang = get_lang()
	[language_data.append([l[0],l[1]]) for l in lang]
	[top_language_data.append([t[0],t[1]]) for t in top_lang] 
	return render_template("lang2.html",
		language_data=language_data, top_language_data=top_language_data)

def get_lang():
	conn = sqlite3.connect(db)
	conn.row_factory = sqlite3.Row 
	c = conn.cursor()

	c.execute("SELECT * from lang_data ORDER BY datetime DESC LIMIT 1")
	result = c.fetchone()
	lang = ast.literal_eval(result['language'])
	top_lang = ast.literal_eval(result['top_language'])
	conn.close()
	return lang, top_lang


@app.route("/top_tweets")
def top_tweets():
	return render_template("top_tweets1.html") 


@app.route("/trends")
def trends():
	return render_template("trends1.html") 


@app.route("/api/trends")
def get_trends_api():
	print("\nGetting trends from database...")
	conn = sqlite3.connect(db)
	conn.row_factory = sqlite3.Row 
	c = conn.cursor()

	c.execute("SELECT * from trend_data ORDER BY datetime DESC LIMIT 10")
	result = c.fetchall()
	
	trend = []
	trend_tweet = []
	datetime_trends = result[0]['datetime']

	for r in result:
		trend.append(r['trend'])
		trend_tweet.append(r['trend_id1'])
		trend_tweet.append(r['trend_id2'])
		trend_tweet.append(r['trend_id3'])

	conn.close()

	return jsonify(trend=trend, 
		trend_tweet=trend_tweet,
		datetime_trends=datetime_trends)


@app.route("/api/top_tweets")
def get_top_tweets_api():
	print("\nGetting top tweets from database...")
	conn = sqlite3.connect(db)
	conn.row_factory = sqlite3.Row 
	c = conn.cursor()

	c.execute("SELECT * from twit_data ORDER BY datetime DESC LIMIT 30")
	result = c.fetchall()
	tweets = []
	datetime_toptweets = result[0]['datetime']
	[ tweets.append(tweet['top_tweet']) for tweet in result ]
	conn.close()

	return jsonify(tweets=tweets, 
		datetime_toptweets=datetime_toptweets)

