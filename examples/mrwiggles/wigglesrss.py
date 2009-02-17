#!/usr/bin/env python
import re
import urllib

from BeautifulSoup import BeautifulSoup

from hand import BaseFeedGenerator

class WigglesFeed(BaseFeedGenerator):

    def __init__(self, config_file):
        BaseFeedGenerator.__init__(self, config_file)

    def generate_data(self):
        data = urllib.urlopen("http://www.mrwiggleslovesyou.com")
        page = BeautifulSoup(data.read(), fromEncoding='iso-8859-1')
        src = page.find('img', src=re.compile("comics/rehab(\d+)\.jpg"))['src']
        currentstrip = int(src[-7:-4])

        urltemplate = "http://www.mrwiggleslovesyou.com/rehab%d.html"
        imgtemplate = "http://www.mrwiggleslovesyou.com/comics/rehab%d.jpg"

        entries = []
        for stripnumber in xrange(currentstrip - 7, currentstrip + 1):
            day = {}
            day['title'] = "Comic #%d" % stripnumber
            day["page_link"] = urltemplate % stripnumber
            day["guid"] = day['page_link']
            data = urllib.urlopen(urltemplate % stripnumber)
            day["description"] = self.generate_description(imgtemplate % stripnumber)
            day["pubDate"] = data.headers['Last-Modified']
            entries.append(day)
        return reversed(entries)

if __name__ == "__main__":
    wf = WigglesFeed("config.ini")
    wf.process()
