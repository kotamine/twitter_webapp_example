import sqlite3

db = "twitter_data.db"

conn = sqlite3.connect(db)
c = conn.cursor()

try:
	c.execute("drop table trend_data")
	print('trend_data table initialized')
except:
	pass

try:
	c.execute("drop table twit_data")
	print('twit_data table initialized')
except:
	pass

try:
	c.execute("drop table lang_data")
	print('lang_data table initialized')
except:
	pass

try:
	cmd = "CREATE TABLE twit_data (top_tweet TEXT, datetime TEXT)"
	c.execute(cmd)

	cmd = "CREATE TABLE lang_data (language TEXT, top_language TEXT, datetime TEXT)"
	c.execute(cmd)

	cmd = "CREATE TABLE trend_data (trend TEXT, trend_id1 TEXT, trend_id2 TEXT, trend_id3 TEXT, datetime TEXT)"
	c.execute(cmd)

	conn.commit()
	print("creating new tables")
except:
	pass
finally:
	conn.close()

