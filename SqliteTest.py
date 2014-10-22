#!/usr/bin/env python

import feedparser
import sqlite3

conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS podcasts (id INTEGER PRIMARY KEY, feed_addrs TEXT, etag TEXT, modified TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS shows (mp3_link TEXT, title TEXT, description TEXT, length TEXT, pubDate TEXT)''')

def subscribe_Test(feed):
	parse_feed = feedparser.parse(feed)
	if ('etag' or 'modified') in parse_feed.headers:
		feed_etag = parse_feed.etag
		feed_modified = parse_feed.modified
	else:
		feed_etag = None
		feed_modified = None
		
	cur.execute("INSERT INTO podcasts (feed_addrs, etag, modified) VALUES (?, ?, ?)", (feed, feed_etag, feed_modified))
	
	for show in parse_feed.entries:
		mp3_addrs = show.enclosures[0]['href']
		show_title = show.title
		show_desc = show.description
		show_length = show.enclosures[0]['length']
		show_pubDate = show.pubDate
		
		cur.execute("INSERT INTO shows (mp3_link, title, description, length, pubDate) VALUES (?, ?, ?, ?, ?)", 
					(mp3_addrs, show_title, show_desc, show_length, show_pubDate)) 
	conn.commit()
	
def show_Podcasts():
	results = cur.execute("SELECT * FROM podcasts")
	print '\n'
	for row in results:
		print row[0], '\t', row[1], '\t', row[2], '\t', row[3] 
	
if __name__ == "__main__":
	
	#for addrs in open('/home/chuck/Documents/Podcast_list', 'r'):
		#subscribe_Test(addrs)
		
	while True:
		in_feed = raw_input('Enter feed address or (q) to quit: ')
		if in_feed == 'q':
			break
		else:
			subscribe_Test(in_feed)
	show_Podcasts()
	
	
