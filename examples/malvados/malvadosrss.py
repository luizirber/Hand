#!/usr/bin/env python
import re
import urllib

from BeautifulSoup import BeautifulSoup

from hand import BaseFeedGenerator

def try_download(url):
    data = urllib.urlopen(url)
    if data.headers['Content-Type'] == "image/gif" :
        return True
    return False

class MalvadosFeed(BaseFeedGenerator):

    def __init__(self, config_file):
        BaseFeedGenerator.__init__(self, config_file)

    def generate_description(self, page):
        [script.extract() for script in page.findAll('script')]
        imgs = page.findAll('img')
        for img in imgs:
            img['src'] = 'http://www.malvados.com.br/%s' % img['src']
        root = page.find("table")
        return ''.join(["<![CDATA[", root.prettify(), "]]>"])

    def generate_data(self):
        data = urllib.urlopen("http://www.malvados.com.br")
        page = BeautifulSoup(data.read(), fromEncoding='iso-8859-1')
        src = page.find('frame', attrs = {'name':"mainFrame"})['src']
        currentstrip = int(src[5:-5])
        urltemplate = "http://www.malvados.com.br/index%d.html"
        imgtemplate = "http://www.malvados.com.br/tirinha%d.gif"
        logotemplate = "http://www.malvados.com.br/logo%d.gif"

        entries = []
        for stripnumber in xrange(currentstrip - 7, currentstrip + 1):
            day = {}
            if try_download(imgtemplate % stripnumber):
                day['title'] = "Tirinha #%d" % stripnumber
                day["page_link"] = urltemplate % stripnumber
                day["guid"] = day['page_link']

                data = urllib.urlopen(urltemplate % stripnumber)
                page = BeautifulSoup(data.read(), fromEncoding='iso-8859-1')
                day["description"] = self.generate_description(page)
                day["pubDate"] = data.headers['Last-Modified']
            entries.append(day)
        return reversed(entries)

if __name__ == "__main__":
    mf = MalvadosFeed("config.ini")
    mf.process()
