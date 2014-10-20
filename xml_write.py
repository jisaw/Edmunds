import xml.etree.cElementTree as ET
from xml.dom import minidom

def makexml(c, url):
	name = '%s.xml' % url[7:]
	name = name.replace("/", "_")
	t = c.get_tags()
	p = c.get_posts()

	thread = ET.Element('thread')

	orig_poster = ET.SubElement(thread, "orig_poster")
	orig_poster.text = c.get_orig_poster()

	posted_at_date = ET.SubElement(thread, "posted_at_date")
	posted_at_date.text =c.get_posted_at_date()

	posted_at_datetime = ET.SubElement(thread, "posted_at_datetime")
	posted_at_datetime.text = c.get_posted_at_datetime()

	views = ET.SubElement(thread, "views")
	views.text = c.get_views()

	replies = ET.SubElement(thread, "replies")
	replies.text = c.get_replies()

	lastposted_date = ET.SubElement(thread, "lastposted_date")
	lastposted_date.text = c.get_lastposted_date()

	lasposted_datetime = ET.SubElement(thread, "lasposted_datetime")
	lasposted_datetime.text = c.get_lasposted_datetime()

	tags = ET.SubElement(thread, "tags")

	for i in range(len(tags)):
		tags.text = t[i]

	posts = ET.SubElement(thread, "posts")

	for i in range(len(p)):
		username = ET.SubElement(posts, "username")
		username.text = p[i][0]
	
		date = ET.SubElement(posts, "date")
		date.text = p[i][1]
	
		body = ET.SubElement(posts, "body")
		body.text = p[i][2]

	f = open('../../data/' + name, 'w')
	with f:
		tree = ET.ElementTree(thread)
		tree.write(f)
		print("\nXML WRITTEN!!")
	f.close()


def prettify(elem):
	rough_string = ElementTree.tostring(elem, 'utf-8')
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml(indent=" ")