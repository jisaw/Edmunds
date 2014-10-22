from bs4 import BeautifulSoup
import requests
import constants
import thread_level as tl
import post_level as pl
from constants import xmlout
import xml_write as xw
import re
import sys
from xmloutput import xmlout

def main():
	for url in constants.urls_urls:
		urls = []
		r = requests.get(url)
		data = r.text
		soup = BeautifulSoup(data)
		lp = soup.find('a', class_ = re.compile('^LastPage'))
		try:
			for i in range(int(lp.string)):
				new_num = lp['href'].find('=')+1
				new_end = lp['href'][:new_num] + 'p%s&' % (i+1) 
				new_url = 'http://forums.edmunds.com' + new_end
				if new_url not in urls:
					print(new_url)
					urls.append(new_url)
				else: 
					print('Duplicate Link')
		except:
			print('\n\n  ERROR  \n\n')
	metaDataExtraction(urls)

def metaDataExtraction(urls):
	for url in urls:
		r = requests.get(url)
		data = r.text
		soup = BeautifulSoup(data)

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

		threadUrls = tl.get_post_level(soup)
	
		dataAngel = xmlout()
	
		for i in range(len(date_title)):
			print(original_posters[i])
			dataAngel.set_orig_poster(original_posters[i])
			print(date_title[i])
			dataAngel.set_posted_at_date(date_title[i])
			print(date_dt[i])
			dataAngel.set_posted_at_datetime(date_dt[i])
			print(views[i])
			dataAngel.set_views(views[i])
			print(replies[i])
			dataAngel.set_replies(replies[i])
			print(lp_title[i])
			dataAngel.set_lastposted_date(lp_title[i])
			print(lp_dt[i])
			dataAngel.set_lastposted_datetime(lp_dt[i])

			postPageExtraction(threadUrls[i], dataAngel)

		



def postPageExtraction(url, dataAngel):
	urls = []
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)
	lp = soup.find('a', class_ = re.compile('^LastPage'))
	try:
		for i in range(int(lp.string)):
			new_num = lp['href'].find('=')+1
			new_end = lp['href'][:new_num] + 'p%s&' % (i+1) 
			new_url = 'http://forums.edmunds.com' + new_end
			if new_url not in urls:
				print(new_url)
				urls.append(new_url)
			else: 
				print('Duplicate Link')
	except:
		print('\n\n  ERROR  \n\n')
	tags = pl.get_tags(soup)
	dataAngel.set_tags(tags)

	posts = postExtraction(urls)

	dataAngel.set_posts(posts)

	xml_write(dataAngel, url, sys.argv[1])


def postExtraction(urls):
	posts = []
	for url in urls:
		r = requests.get(url)
		data = r.text
		soup = BeautifulSoup(data)

		bodies = pl.get_post_body(soup)
		users = pl.get_post_user(soup)
		dates = pl.get_post_date(soup)
		for i in range(len(bodies)):
			posts.append([users[i], dates[i], bodies[i]])
	return posts


#def threadLevelSoup(soup, url):
#	soups = []
#	urls = []
#	for url in tl.get_post_level(soup):
#		r = requests.get(url)
#		data = r.text
#		urls.append(url)
#		soups.append(BeautifulSoup(data))
#
#	original_posters = tl.get_original_posters(soup)
#
#	dates = tl.get_date(soup)
#	date_title = dates[0]
#	lp_title = dates[1]
#
#	datetimes = tl.get_datetimes(soup)
#	date_dt = datetimes[0]
#	lp_dt = datetimes[1]
#
#	nums = tl.get_nums(soup)
#	replies = nums[0]
#	views = nums[1]
#
#	
#
#		print("urlsing Post Level")
#		print(urls[i])
#		postLevelSoup(soups[i], urls[i])
#
#		print("urlsing XML Writer")
#
#		xw.makexml(dataAngel, url, sys.argv[1])
#
#	
#		
#
#
#def postLevelSoup(soup, url):
#	urls = []
#	posts = []
#	tags = pl.get_tags(soup)
#	print(tags)
#
#	bodies = pl.get_post_body(soup)
#	users = pl.get_post_user(soup)
#	dates = pl.get_post_date(soup)
#
#	lp = soup.find('a', class_ = re.compile('^LastPage'))
#	try:
#		#links = lp.find('a')
#		#for link in links:
#		#	new_url = link['href']
#		#	if new_url not in urls:
#		#		print(new_url)
#		#		urls.append(new_url)
#		#	else:
#		#		print('Duplicate Link')
#		for i in range(int(lp.string)):
#				new_num = lp['href'].find('=')+1
#				new_end = lp['href'][:new_num] + 'p%s&' % (i+1) 
#				new_url = new_end
#				if new_url not in urls:
#					print(new_url)
#					urls.append(new_url)
#				else: 
#					print('Duplicate Link')
#	except:
#		print('\n\n ERROR \n\n')
#	for url in urls:
#		r = requests.get(url)
#		data = r.text
#		soup = BeautifulSoup(data)
#		bodies = pl.get_post_body(soup)
#		users = pl.get_post_user(soup)
#		dates = pl.get_post_date(soup)
#		for i in range(len(bodies)):
#			posts.append([users[i], dates[i], bodies[i]])
#
#	dataAngel.set_tags(tags)
#	dataAngel.set_posts(posts)


if __name__ == "__main__":
	main()#