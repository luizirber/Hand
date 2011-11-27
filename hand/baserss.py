#!/usr/bin/env python
from os.path import expanduser
from datetime import date, timedelta, datetime
from StringIO import StringIO
import rfc822
from ConfigParser import ConfigParser
from string import Template
import codecs
import re, htmlentitydefs

from shove import Shove

today = date(2000,1,1).today()

class BaseFeedGenerator(object):

    def __init__(self, config_file=None):
        #configs = config
        self.conf = {}
        if config_file:
            config = ConfigParser()
            config.read(config_file)

            for option in config.options('Feed'):
                self.conf[option] = config.get('Feed', option)

    def build_date(self, theTime):
        data = rfc822.parsedate_tz(theTime.strftime("%a, %d %b %Y %H:%M:%S"))
        return rfc822.formatdate(rfc822.mktime_tz(data))

    def unescape(self, text):
        '''Removes HTML or XML character references and entities from a text string.

        from: http://effbot.org/zone/re-sub.htm#unescape-html

        @param text The HTML (or XML) source text.
        @return The plain text, as a Unicode string, if necessary.'''

        def fixup(m):
            text = m.group(0)
            if text[:2] == "&#":
                # character reference
                try:
                    if text[:3] == "&#x":
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except ValueError:
                    pass
            else:
                # named entity
                try:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                except KeyError:
                    pass
            return text # leave as is
        return re.sub("&#?\w+;", fixup, text)

    def generate_description(self, link):
        return '<![CDATA[<img src="%s"><br /><br />]]>' % (link)

    def build_feed(self, data):
        feed = StringIO(u'')
        pubDate = self.build_date(datetime(1,1,1).now())
        try:
            template_data = codecs.open(self.conf['template_file'], 'r', 'utf-8')
            template = Template(template_data.read())
            template_data.close()
        except:
            print 'error' #TODO: tratar erro!
        base = template.substitute(self.conf, pubDate=pubDate, lastBuildDate=pubDate)
        feed.write(base)

        feed.write('    <skipHours>\n')
        build_hours = [int(i) for i in self.conf['build_hours'].split(',')]
        for skip in xrange(0,24):
            if skip not in build_hours:
                feed.write('      <hour>%d</hour>\n'% skip)
        feed.write('    </skipHours>\n')

        for entry in data:
            if date(*rfc822.parsedate(entry['pubDate'])[:3]) <= today:
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

    def save_data(self, data):
        db = Shove(self.conf['data_file'])
        modified = False
        for item in data:
            try:
                db[item['guid']]
            except KeyError:
                db[item['guid']] = item
                modified = True
            else:
                if db[item['guid']] != item:
                    db[item['guid']] = item
                    modified = True
        db.close()
        return modified

    def process(self):
        data = list(self.generate_data())
        if self.save_data(data):
        #if 1:
            rss_feed = self.build_feed(data)
            rss_file = codecs.open(self.conf['output_file'], 'w+', 'utf-8')
            rss_file.write(rss_feed)
