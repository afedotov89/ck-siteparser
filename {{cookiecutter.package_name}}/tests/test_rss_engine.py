# -*- coding: utf-8 -*-
import os
from unittest import TestCase

from siteparser.engine.rss import RSSEngine, RSSConfig


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestRSS(TestCase):

    def test_vesti(self):
        rss = open(os.path.join(CURRENT_DIR, 'vesti.rss')).read()
        engine = RSSEngine(RSSConfig())
        entries = engine.process(rss)
        self.assertEqual(next(entries)['link'], 'https://www.vesti.ru/doc.html?id=2986503')
        for entry in engine.process(rss):
            print(entry)

    def test_nplus1(self):
        rss = open(os.path.join(CURRENT_DIR, 'nplus1.rss')).read()
        engine = RSSEngine(RSSConfig())
        entries = engine.process(rss)
        self.assertEqual(next(entries)['image'], 'https://nplus1.ru/images/2018/02/10/d69903c4dc4b0a6d22816cdeb1439116.gif')



