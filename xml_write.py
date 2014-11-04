import xml.etree.cElementTree as ET
from xml.dom import minidom
import os


def makexml(dataAngel, url, folder, make):
    # Formats the name for the file
    name = '%s.xml' % url[7:]
    name = name.replace("/", "_")

    prefix = '../../data/%s/%s/' % (folder, make)
    #prefix = '%s/' % ( make)
    t = dataAngel.get_tags()
    p = dataAngel.get_posts()

    #This is the creation of the XML tree
    thread = ET.Element('thread')

    orig_poster = ET.SubElement(thread, "orig_poster")
    orig_poster.text = dataAngel.get_orig_poster()

    posted_at_date = ET.SubElement(thread, "posted_at_date")
    posted_at_date.text = dataAngel.get_posted_at_date()

    posted_at_datetime = ET.SubElement(thread, "posted_at_datetime")
    posted_at_datetime.text = dataAngel.get_posted_at_datetime()

    views = ET.SubElement(thread, "views")
    views.text = dataAngel.get_views()

    replies = ET.SubElement(thread, "replies")
    replies.text = dataAngel.get_replies()

    lastposted_date = ET.SubElement(thread, "lastposted_date")
    lastposted_date.text = dataAngel.get_lastposted_date()

    lasposted_datetime = ET.SubElement(thread, "lasposted_datetime")
    lasposted_datetime.text = dataAngel.get_lasposted_datetime()

    tags = ET.SubElement(thread, "tags")
    tag_list = []
    for i in range(len(t)):
        tag_list.append(t[i])
    tags.text = ", ".join(tag_list)

    posts = ET.SubElement(thread, "posts")

    for i in range(len(p)):
        username = ET.SubElement(posts, "username")
        username.text = p[i][0]

        date = ET.SubElement(posts, "date")
        date.text = p[i][1]

        body = ET.SubElement(posts, "body")
        body.text = p[i][2]

    f = open(prefix + name, 'w')
    with f:
        tree = ET.ElementTree(thread)
        #tree = prettify(tree)
        tree.write(f)
        print("\nXML WRITTEN!!")
    f.close()

# A method to prettify the XML --Curently not in use
def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent=" ")