# -*- coding: utf-8 -*-
from datetime import datetime
from time import mktime

import feedparser
import re


class RSSEngine(object):

    IMG_TYPE_REGEXP = re.compile('image|img', re.I)

    def __init__(self, config):
        self.config = config

    def process(self, url):
        d = feedparser.parse(url)
        # title = d['feed']['title']
        for entry in d.entries:
            res = {}
            if hasattr(entry, 'title'):
                res[self.config.title_field] = entry.title
            if hasattr(entry, 'description'):
                res[self.config.description_field] = entry.description
            if hasattr(entry, 'link'):
                link = entry.link
                if hasattr(entry, 'yandex_related'):
                    if link == entry.links[-1].get('href'):
                        link = entry.links[0].get('href')
                res[self.config.link_field] = link
            if hasattr(entry, 'published_parsed'):
                published = datetime.fromtimestamp(mktime(entry.published_parsed))
                res[self.config.published_field] = published
            if hasattr(entry, 'enclosures'):
                img_enclosures = [
                    e for e in entry.enclosures if self.IMG_TYPE_REGEXP.search(e.get('type', ''))
                ]
                if img_enclosures:
                    res[self.config.image_field] = img_enclosures[0]['href']
            if hasattr(entry, 'media_content'):
                url = entry.media_content[0].get('url')
                if url:
                    res[self.config.image_field] = url
            yield res


class RSSConfig(object):
    description_field = 'description'
    title_field = 'title'
    published_field = 'published'
    link_field = 'link'
    image_field = 'image'


