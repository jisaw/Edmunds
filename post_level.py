from bs4 import BeautifulSoup
import requests
import re
import string
from lxml import html


def get_post_body(soup):
    bodies = []
    bod = []
    b = soup.find_all(class_='Message')
    for body in b:
        bodies.append(''.join(body.stripped_strings))
    return bodies


def get_post_user(soup):
    usernames = []
    username = soup.find_all(class_='Username')
    for user in username:
        usernames.append(user.string)
    return usernames


def get_post_date(soup):
    dates = []
    d = soup.find_all('time')
    for date in d:
        dates.append(date['datetime'])
    return dates


def get_tags(tree):
    tags = []
    meta_tags = tree.xpath("//div[@class='InlineTags Meta']/ul/li/a/text()")
    # t = meta_tags.find_all('a')
    for tag in meta_tags:
        tags.append(tag)
    return tags
