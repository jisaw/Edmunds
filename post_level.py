from bs4 import BeautifulSoup
import requests
import re
import string

def get_post_body(soup):
	bodies = []
	bod = []
	b = soup.find_all(class_ = 'Message')
	for body in b:
		bodies.append(''.join(body.stripped_strings))
	return bodies

def get_post_user(soup):
	usernames = []
	u = soup.find_all(class_ = 'Username')
	for user in u:
		usernames.append(user.string)
	return usernames

def get_post_date(soup):
	dates = []
	d = soup.find_all('time')
	for date in d:
		dates.append(date['datetime'])
	return dates

def get_tags(soup):
	tags = []
	t = soup.find_all('a', class_ = re.compile('^Tag'))
	for tag in t:
		tags.append(tag.string)
	return tags
