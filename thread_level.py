from bs4 import BeautifulSoup
import requests


def get_post_level(soup):
    urls = []
    threads = soup.find_all(class_='Title')
    for thread in threads:
        print(thread['href'])
        urls.append(thread['href'])
    return urls


def get_original_posters(soup):
    posters = []
    p = soup.find_all(class_='UserLink BlockTitle')
    for username in p:
        posters.append(username.string)
    return posters


def get_date(soup):
    all_nums = []
    dates = []
    last_posted = []
    d = soup.find_all('time')
    for date in d:
        all_nums.append(date['title'])
    for x in range(len(all_nums)):
        if x % 2 == 0:
            last_posted.append(all_nums[x])
        else:
            dates.append(all_nums[x])
    return (dates, last_posted)


def get_datetimes(soup):
    all_nums = []
    datetimes = []
    last_posted_datetimes = []
    dt = soup.find_all('time')
    for date in dt:
        all_nums.append(date['datetime'])
    for x in range(len(all_nums)):
        if x % 2 == 0:
            datetimes.append(all_nums[x])
        else:
            last_posted_datetimes.append(all_nums[x])
    return (datetimes, last_posted_datetimes)


def get_nums(soup):
    all_nums = []
    replies = []
    views = []
    r = soup.find_all(class_='Number')
    for i in r:
        all_nums.append(i.text)
    for x in range(len(all_nums)):
        if x % 2 == 0:
            replies.append(all_nums[x])
        else:
            views.append(all_nums[x])
    return (replies, views)