from bs4 import BeautifulSoup
import constants
import thread_level as tl
import post_level as pl
import xml_write as xw
import requests
import re
import sys
from xml_output import xmlout
from urllib import urlopen
import os
from lxml import html
import datetime


#Takes in the command line argument immediatly after main.py and creates
#a folder with that name in the data directory
folder = sys.argv[1]

current_dir = os.getcwd()
#os.chdir("/home/research/projects/edmunds/data")
os.system("mkdir %s" % folder)
os.chdir(current_dir)


#This starts with the constant urls and creates a list of all the thread level pages
def main():
  print('starting main')
  print datetime.datetime.now().strftime('%H:%M:%S')
  dataAngel = xmlout()
  for i in range(len(constants.start_urls)):
  #for url in constants.start_urls:
    print('for i in range(len(constants.start_urls))')
    print datetime.datetime.now().strftime('%H:%M:%S')
    make = constants.MAKES[i]
    #os.chdir("/home/research/projects/edmunds/data/%s" % folder)
    os.system("mkdir %s" % make)
    os.chdir(current_dir)

    urls = []
    print('Crated make folder')
    print datetime.datetime.now().strftime('%H:%M:%S')
    r = requests.get(constants.start_urls[i])
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    print('soup opened')
    print datetime.datetime.now().strftime('%H:%M:%S')
    lp = soup.find('a', class_=re.compile('^LastPage'))
    if (lp is not None):
        for i in range(int(lp.string)):
            try:
                print('with lp try')
                print datetime.datetime.now().strftime('%H:%M:%S')
                new_num = lp['href'].find('=') + 1
                new_end = lp['href'][:new_num] + 'p%s&' % (i + 1)
                new_url = 'http://forums.edmunds.com' + new_end
                print('Created new url')
                print datetime.datetime.now().strftime('%H:%M:%S')
                if new_url not in urls:
                  print(new_url)
                  urls.append(new_url)
                  print('Added URL')
                  print datetime.datetime.now().strftime('%H:%M:%S')
                else:
                  print('Duplicate Link')
            except:
              print('\n\n  ERROR  \n\n')
              print datetime.datetime.now().strftime('%H:%M:%S')
        print('calling metaDataExtraction')
        print datetime.datetime.now().strftime('%H:%M:%S')
        metaDataExtraction(urls, dataAngel, make)
        print('metaDataExtraction finished')
        print datetime.datetime.now().strftime('%H:%M:%S')

#Is run on every thread level page. it scrapes the meta data, adds it to the dataAngel class, and then passes the links along for the post level scraping
def metaDataExtraction(urls, dataAngel, make):
  for url in urls:
    print(url)
    print('getting meta data')
    print datetime.datetime.now().strftime('%H:%M:%S')
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    tree = html.fromstring(data)

    original_posters = tl.get_original_posters(tree)

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
      print('calling postPageExtraction')
      print datetime.datetime.now().strftime('%H:%M:%S')
      postPageExtraction(threadUrls[i], dataAngel, make)
      print('finished postPageExtraction')
      print datetime.datetime.now().strftime('%H:%M:%S')

#This is where all of the post level pages are added to a list to be iterated over. Also the tags are scraped and stored in the dataAngel class with the other information
def postPageExtraction(url, dataAngel, make):
  urls = []
  print(url)
  r = requests.get(url)
  data = r.text
  soup = BeautifulSoup(data, 'lxml')
  tree = html.fromstring(data)
  try:
    lp = soup.find('a', class_=re.compile('^LastPage'))
  except:
    print('')
  if (lp is not None):
    for i in range(int(lp.string)):
      try:
        #if int(lp.string) > 100:
        #print ('\n\n Skipping \n\n')
        #else:
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
    tags = pl.get_tags(tree)
    dataAngel.set_tags(tags)

  print('calling postExtraction')
  print datetime.datetime.now().strftime('%H:%M:%S')
  postExtraction(urls, dataAngel, url, make)
  print('postExtraction finished')
  print datetime.datetime.now().strftime('%H:%M:%S')

#Finally. this is where the posts themselves are scraped. They are also added to the dataAngel class and passed to the xml writing script.
def postExtraction(urls, dataAngel, name_url, make):
  posts = []
  for url in urls:
    try:
      print('Got url: ' + url)
      r = requests.get(url)
      data = r.text
      soup = BeautifulSoup(data, 'lxml')
      tree = html.fromstring(data)
      bodies = pl.get_post_body(tree)
      print('Got bodies')
      users = pl.get_post_user(tree)
      print('Got users')
      dates = pl.get_post_date(tree)
      print('Got dates')
      print('\n\n\n\n\n\n\n usr: %s \ndate: %s \nbod: %s' % (len(users), len(dates), len(bodies)))
      for i in range(len(users)):
        posts.append([users[i], dates[i], bodies[i]])
    except:
      print("\n\nERROR\n\n")
  dataAngel.set_posts(posts)
  print('calling makexml')
  print datetime.datetime.now().strftime('%H:%M:%S')
  xw.makexml(dataAngel, name_url, folder, make)
  print('xml written')
  print datetime.datetime.now().strftime('%H:%M:%S')

if __name__ == "__main__":
  main()