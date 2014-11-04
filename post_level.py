from bs4 import BeautifulSoup
import requests
import re
import string
from lxml import html


def get_post_body(tree):
    bodies = []
    bod = []
    b = tree.xpath("//div[@class='Comment']/dic[@class='Message']/p/text()")
    for body in b:
        bodies.append(body)
    return bodies


def get_post_user(tree):
    usernames = []
    username = tree.xpath("//div[@class='Comment']/span[@class='Author']/a[@class='Username']/text()")
    for user in username:
        usernames.append(user)
    return usernames


def get_post_date(tree):
    dates = []
    d = tree.xpath("//div[@class='Comment']/div[@class='Meta CommentMeta CommentInfo']/span/a/time/@title")
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
