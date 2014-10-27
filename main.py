from bs4 import BeautifulSoup
import constants
import thread_level as tl
import post_level as pl
import xml_write as xw
import re
import sys
from xml_output import xmlout
from urllib import urlopen
import os

folder = sys.argv[1]

current_dir = os.getcwd()
os.chdir("/home/research/projects/edmunds/data")
os.system("mkdir %s" % folder)
os.chdir(current_dir)


def main():
  for url in constants.start_urls:
    urls = []
    r = urlopen(url)
    soup = BeautifulSoup(r, 'lxml')
    lp = soup.find('a', class_=re.compile('^LastPage'))
    try:
      for i in range(int(lp.string)):
        new_num = lp['href'].find('=') + 1
        new_end = lp['href'][:new_num] + 'p%s&' % (i + 1)
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
    print(url)
    r = urlopen(url)
    soup = BeautifulSoup(r, 'lxml')

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
      print(threadUrls[i])
      postPageExtraction(threadUrls[i], dataAngel)


def postPageExtraction(url, dataAngel):
  urls = []
  print(url)
  r = urlopen(url)
  soup = BeautifulSoup(r, 'lxml')
  lp = soup.find('a', class_=re.compile('^LastPage'))
  try:
    if int(lp.string) > 100:
      print ('\n\n Skipping \n\n')
    else:
      for i in range(int(lp.string)):
        link = lp['href']
        num = len(lp.string) + 1
        new_url = link[:-num] + 'p%s' % (i + 1)
        if new_url not in urls:
          print(new_url)
          urls.append(new_url)
        else:
          print('Duplicate Link')
  except:
    print('\n\n  ERROR  \n\n')
  tags = pl.get_tags(soup)
  dataAngel.set_tags(tags)

  postExtraction(urls, dataAngel, url)


def postExtraction(urls, dataAngel, name_url):
  posts = []
  try:
    for url in urls:
      print('Got url: ' + url)
      r = urlopen(url)
      soup = BeautifulSoup(r, 'lxml')

      bodies = pl.get_post_body(soup)
      print('Got bodies')
      users = pl.get_post_user(soup)
      print('Got users')
      dates = pl.get_post_date(soup)
      print('Got dates')
      for i in range(len(bodies)):
        posts.append([users[i], dates[i], bodies[i]])
      r.close()
  except:
    print("\n\nERROR\n\n")
  dataAngel.set_posts(posts)
  xw.makexml(dataAngel, name_url, folder)


# def threadLevelSoup(soup, url):
# soups = []
# urls = []
# for url in tl.get_post_level(soup):
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
  main()  #