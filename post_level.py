from bs4 import BeautifulSoup
import requests
import re
import string
from lxml import html


def get_post_body(tree):
    bodies = []
    bod = []
    #b = soup.find_all(class_='Message')
    b = tree.xpath("//div[@class='Message']")
    for body in b:
        bodies.append(body.xpath('./p/text()'))
    return bodies


def get_post_user(tree):
    usernames = []
    #username = soup.find_all(class_='Username')
    username = tree.xpath('//a[@class="Username"]/text()')
    for user in username:
        usernames.append(user)
    return usernames


def get_post_date(tree):
    dates = []
    #d = soup.find_all('time')
    d = tree.xpath("//a[@class='Permalink']/time/@title")
    for date in d:
        dates.append(date)
    return dates


def get_tags(tree):
    tags = []
    meta_tags = tree.xpath("//div[@class='InlineTags Meta']/ul/li/a/text()")
    # t = meta_tags.find_all('a')
    for tag in meta_tags:
        tags.append(tag)
    return tags
