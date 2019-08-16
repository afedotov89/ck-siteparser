# Sample Test passing with nose and pytest
from __future__ import print_function
from unittest import TestCase

from siteparser.parser import Parser


class TestRSS(TestCase):

    def test_rss(self):
        url = 'https://hightech.fm/feed.rss'
        print(url)
        parser = Parser()
        for p in parser.rss(url):
            print(p.document)






