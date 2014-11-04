from bs4 import BeautifulSoup
import requests
import re
import string
import lxml


def get_post_body(soup):
    bodies = []
    bod = []
    b = soup.find_all(class_='Message')
    for body in b:
        bodies.append(''.join(body.stripped_strings))
    return bodies


def get_post_user(tree):
    usernames = []
    username = tree.xpath("//a[@class='Username']/text()")
    for user in username:
        usernames.append(user)
    return usernames


def get_post_date(tree):
    dates = []
    d = tree.xpath('//div/a[@class = "Permalink"]/time/@title')
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
