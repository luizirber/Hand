#!/usr/bin/env python
import re
import urllib

from BeautifulSoup import BeautifulSoup

from hand import BaseFeedGenerator

class OOTSFeed(BaseFeedGenerator):

    def __init__(self, config_file):
        BaseFeedGenerator.__init__(self, config_file)

    def generate_data(self):
        BASE = "http://www.giantitp.com/"
        PAGE_LINK_TEMPLATE = BASE + "comics/oots%04d.html"
        data = urllib.urlopen(BASE + "comics/oots0631.html")
        page = BeautifulSoup(data.read(), fromEncoding='iso-8859-1')
        latest = page.find('img', alt='Latest Comic')
        latest_link = latest.findParent()['href']
        data.close()

        currentstrip = int(latest_link[-9:-5])
        entries = []
        for stripnumber in xrange(currentstrip - 7, currentstrip + 1):
            day = {}
            day['title'] = "Comic #%d" % stripnumber
            day["page_link"] = PAGE_LINK_TEMPLATE % stripnumber
            day["guid"] = day['page_link']
            data = urllib.urlopen(PAGE_LINK_TEMPLATE % stripnumber)
            page = BeautifulSoup(data.read(), fromEncoding='iso-8859-1')
            img_link = page.find('img', src=re.compile("comics/images/."))
            day["description"] = self.generate_description(BASE[:-1] + img_link['src'])
            day["pubDate"] = data.headers['Last-Modified']
            entries.append(day)
        return reversed(entries)

if __name__ == "__main__":
    of = OOTSFeed("config.ini")
    of.process()
