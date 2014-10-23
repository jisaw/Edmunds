class xmlout:
  # orig_poster = ""
  # posted_at_date = ""
  #posted_at_datetime = ""
  #views = ""
  #replies = ""
  #lastposted_date = ""
  #lasposted_datetime = ""
  #tags = ""
  #posts = ""


  def __init__(self):
    self.orig_poster = ""
    self.posted_at_date = ""
    self.posted_at_datetime = ""
    self.views = ""
    self.replies = ""
    self.lastposted_date = ""
    self.lasposted_datetime = ""
    self.tags = []
    self.posts = []

  def set_orig_poster(self, value):
    self.orig_poster = value

  def set_posted_at_date(self, value):
    self.posted_at_date = value

  def set_posted_at_datetime(self, value):
    self.posted_at_datetime = value

  def set_views(self, value):
    self.views = value

  def set_replies(self, value):
    self.replies = value

  def set_lastposted_date(self, value):
    self.lastposted_date = value

  def set_lastposted_datetime(self, value):
    self.lasposted_datetime = value

  def set_tags(self, value):
    self.tags = value

  def set_posts(self, value):
    self.posts = value

  def get_orig_poster(self):
    return self.orig_poster

  def get_posted_at_date(self):
    return self.posted_at_date

  def get_posted_at_datetime(self):
    return self.posted_at_datetime

  def get_views(self):
    return self.views

  def get_replies(self):
    return self.replies

  def get_lastposted_date(self):
    return self.lastposted_date

  def get_lasposted_datetime(self):
    return self.lasposted_datetime

  def get_tags(self):
    return self.tags

  def get_posts(self):
    return self.posts