#!/usr/bin/env python
import re
from datetime import date, timedelta

import mechanize
from BeautifulSoup import BeautifulSoup

from hand import BaseFeedGenerator

class FSPFeed(BaseFeedGenerator):

    def __init__(self, config_file):
        BaseFeedGenerator.__init__(self, config_file)

    def generate_data(self):
        br = mechanize.Browser()

        # connect to the UOL login page
        br.open("https://acesso.uol.com.br/login.html")
        br.select_form(nr=0)
        # Well, you need a user and password here. Do you want mine?!? =D
        br.form["user"] = ""
        br.form["pass"] = ""
        br.submit()

        BASE = "http://www1.folha.uol.com.br/fsp/quadrin/"
        quadrinho = re.compile(r'f3(\d{2})(\d{2})(\d{4})\d*.htm$')
        quad_image = re.compile(r'(\w{3,4})(\d{2})(\d{2})((\d{4})|(\d{4})(\d{2}))\.(gif|jpg)$')

        today = date(2000,1,1).today()
        current = today - timedelta(7)

        week = []
        while current <= today:
            week.append(current)
            current += timedelta(1)

        entries = []
        for day in reversed(week):
            new_index = ("inde%02i%02i%02i.htm") % (day.day,
                                                    day.month,
                                                    day.year)
            response = br.open(BASE + new_index)
            page = BeautifulSoup(response.read())
            urls = page.findAll("a", href=quadrinho)

            for url in urls:
                response = br.open(BASE + url['href'])
                page = BeautifulSoup(response.read())
                quad_link_rel = page.find("img", src=quad_image)
                quad_link = BASE[:-8] + quad_link_rel['src'][3:]

                entry = {}
                entry['title'] = url.string
                entry['page_link'] = BASE + url['href']
                entry['guid'] = entry['page_link']
                entry['description'] = self.generate_description(quad_link)
                entry['pubDate'] = self.build_date(day)

                entries.append(entry)

        return entries

if __name__ == "__main__":
    ff = FSPFeed('config.ini')
    ff.process()
