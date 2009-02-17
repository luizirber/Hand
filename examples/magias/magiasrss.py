#!/usr/bin/env python
import re
import urllib

from BeautifulSoup import BeautifulSoup

from hand import BaseFeedGenerator

class MagiasFeed(BaseFeedGenerator):

    def __init__(self, config_file):
        BaseFeedGenerator.__init__(self, config_file)

    def generate_data(self):
        quad_link = re.compile("http://www.magiasebarbaridades.com/tiras/.")

        data = urllib.urlopen("http://magiasebarbaridades.blogspot.com")
        page = BeautifulSoup(data.read(), fromEncoding='iso-8859-1')
        data.close()
        image = page.find('img', src=quad_link)
        currentstrip = int(image['src'][-7:-4])

        entries = []
        for stripnumber in xrange(currentstrip - 7, currentstrip + 1):
            day = {}
            day['title'] = "Tirinha #%d" % stripnumber
            page_link = image['src'][:-7] + str(stripnumber) + ".gif"
            day["page_link"] = page_link
            day['guid'] = day["page_link"]
            data = urllib.urlopen(page_link)
            day["description"] = self.generate_description(page_link)
            day["pubDate"] = data.headers['Last-Modified']
            data.close()
            entries.append(day)
        return reversed(entries)

if __name__ == "__main__":
    mf = MagiasFeed("config.ini")
    mf.process()
