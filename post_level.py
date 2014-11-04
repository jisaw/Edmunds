from bs4 import BeautifulSoup
import requests
import re
import string
import lxml


def get_post_body(tree):
    bodies = []
    bod = []
    b = tree.xpath("//div[@class='Item-Body']/div[@class='Message']/text()")
    for body in b:
        bodies.append(''.join(body.stripped_strings))
    return bodies


def get_post_user(tree):
    usernames = []
    username = tree.xpath("//a[@class='Username']/text()")
    for user in username:
        usernames.append(user.string)
    return usernames


def get_post_date(tree):
    dates = []
    d = tree.xpath("//span[@class='MItem DateCreated']/a/time")
    for date in d:
        dates.append(date['datetime'])
    return dates


def get_tags(tree):
    tags = []
    meta_tags = tree.xpath("//div[@class='InlineTags Meta']/ul/li/a/text()")
    t = meta_tags.find_all('a')
    for tag in t:
        tags.append(tag.string)
    return tags
