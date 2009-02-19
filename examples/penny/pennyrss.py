#!/usr/bin/env python
import re
import urllib

from BeautifulSoup import BeautifulSoup

from hand import BaseFeedGenerator

class PennyFeed(BaseFeedGenerator):

    def __init__(self, config_file):
        BaseFeedGenerator.__init__(self, config_file)

    def generate_data(self):
        BASE = "http://www.penny-arcade.com"
        current_page = "/comic"

        entries = []
        for i in xrange(7):
            data = urllib.urlopen(BASE + current_page)
            page = BeautifulSoup(data.read(), fromEncoding='iso-8859-1')
            container = page.find('div', attrs={'class':'simplebody'})
            img = container.contents[0]

            day = {}
            day['title'] = img['alt']
            day['page_link'] = BASE + current_page
            day['guid'] = day['page_link']
            day['description'] = self.generate_description(BASE + img['src'])
            day['pubDate'] = data.headers['Last-Modified']
            entries.append(day)

            previous = page.find('img', title='Back')
            current_page = previous.findParent()['href']

        return entries

if __name__ == "__main__":
    pf = PennyFeed("config.ini")
    pf.process()
