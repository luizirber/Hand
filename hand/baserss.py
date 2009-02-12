#!/usr/bin/env python
from os.path import expanduser
from datetime import date, timedelta, datetime
from cStringIO import StringIO
import rfc822

class BaseFeedGenerator(object):

    def __init__(self):
        pass

    def build_date(self, theTime):
        data = rfc822.parsedate_tz(theTime.strftime("%a, %d %b %Y %H:%M:%S"))
        return rfc822.formatdate(rfc822.mktime_tz(data))

    def generate_description(self, link):
        return '&lt;img src="%s"&gt;&lt;br /&gt;&lt;br /&gt;' % (link)

    def build_feed(self, data):
        feed = StringIO()
        pubDate = self.build_date(datetime(1,1,1).now())
        template = open(self.template_file, 'r').read()
        template = template % (pubDate, pubDate)
        feed.write(template)

        for entry in data:
            feed.write(
               ("""    <item>\n"""
                """      <title>%s</title>\n"""
                """      <link>%s</link>\n"""
                """      <description>%s</description>\n"""
                """      <pubDate>%s</pubDate>\n"""
                """      <guid>%s</guid>\n"""
                """    </item>\n""") % (entry['title'],
                                        entry['page_link'],
                                        entry['description'],
                                        entry['pubDate'],
                                        entry['guid']))

        feed.write("""  </channel>\n""")
        feed.write('</rss>\n')

        return feed.getvalue()

    def generate_data(self):
        raise NotImplementedError

    def process(self):
        data = self.generate_data()
        rss_feed = self.build_feed(data)
        rss_file = open(self.rss_file, 'w+')
        rss_file.write(str(rss_feed))
