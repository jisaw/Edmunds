from bs4 import BeautifulSoup
import requests
import constants
import thread_level as tl
import post_level as pl
from constants import cxml
import xml_write as xw
import re
import sys

def main():
	start = []
	for url in constants.start_urls:
		start.append(url)
		r = requests.get(url)
		data = r.text
		soup = BeautifulSoup(data)
		lp = soup.find_all(rel = 'next')
		for link in lp:
			new_url = url + '?Page=p%s&' % link.string
			start.append(new_url)
	for url in start:
		r = requests.get(url)
		data = r.text
		soup = BeautifulSoup(data)
		print("Starting Thread Level")
		threadLevelSoup(soup, url)

def threadLevelSoup(soup, url):
	soups = []
	urls = []
	for url in tl.get_post_level(soup):
		r = requests.get(url)
		data = r.text
		urls.append(url)
		soups.append(BeautifulSoup(data))

	original_posters = tl.get_original_posters(soup)

	dates = tl.get_date(soup)
	date_title = dates[0]
	lp_title = dates[1]

	datetimes = tl.get_datetimes(soup)
	date_dt = datetimes[0]
	lp_dt = datetimes[1]

	nums = tl.get_nums(soup)
	replies = nums[0]
	views = nums[1]

	for i in range(len(date_title)):
		print(original_posters[i])
		cxml.set_orig_poster(original_posters[i])
		print(date_title[i])
		cxml.set_posted_at_date(date_title[i])
		print(date_dt[i])
		cxml.set_posted_at_datetime(date_dt[i])
		print(views[i])
		cxml.set_views(views[i])
		print(replies[i])
		cxml.set_replies(replies[i])
		print(lp_title[i])
		cxml.set_lastposted_date(lp_title[i])
		print(lp_dt[i])
		cxml.set_lastposted_datetime(lp_dt[i])

		print("Starting Post Level")
		print(urls[i])
		postLevelSoup(soups[i], urls[i])

		print("Starting XML Writer")

		xw.makexml(cxml, url, sys.argv[1])

	
		


def postLevelSoup(soup, url):
	urls = []
	posts = []
	tags = pl.get_tags(soup)

	bodies = pl.get_post_body(soup)
	users = pl.get_post_user(soup)
	dates = pl.get_post_date(soup)

	lp = soup.find_all(rel = 'next')
	for link in lp:
		end = '/%s' % link.string
		new_url = url + end
		print(new_url)
		urls.append(new_url)
	for url in urls:
		r = requests.get(url)
		data = r.text
		soup = BeautifulSoup(data)
		bodies = pl.get_post_body(soup)
		users = pl.get_post_user(soup)
		dates = pl.get_post_date(soup)
		for i in range(len(bodies)):
			posts.append([users[i], dates[i], bodies[i]])

	cxml.set_tags(tags)
	cxml.set_posts(posts)


if __name__ == "__main__":
	main()