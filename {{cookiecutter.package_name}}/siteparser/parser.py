# -*- coding: utf-8 -*-
import requests
import validators

from siteparser.engine.html import HTMLConfig, HTMLEngine, XPathTaker
from siteparser.engine.rss import RSSConfig, RSSEngine
from siteparser.state.base import State
from urllib.parse import urlparse


class Parser(object):

    def __init__(self, user_agent='', proxies=None):
        self.config = Config()
        if user_agent:
            self.config.html.request_headers['User-Agent'] = user_agent
        if proxies:
            self.config.html.proxies = proxies
        self.state = State()
        self.html_engine = None
        self.dom = None

    def rss(self, url):
        engine = RSSEngine(self.config.rss)
        for entity_data in engine.process(url):
            parser = self.clone()
            parser.state.data.update(entity_data)
            yield parser

    def clone(self):
        clone = self.__class__()
        clone.state = self.state.clone()
        clone.config = self.config
        clone.html_engine = self.html_engine
        clone.dom = self.dom
        return clone

    def _is_url(self, url):
        return validators.url(url)

    def fetch(self, url):
        parser = self.clone()
        if not parser.html_engine:
            parser.html_engine = HTMLEngine(self.config.html)
        parser.dom = parser.html_engine.load_dom(url)
        return parser

    def html(self, source):
        parser = self.clone()
        if not parser.html_engine:
            parser.html_engine = HTMLEngine(self.config.html)
        if self._is_url(source):
            parser.dom = parser.html_engine.load_dom(source)
        else:
            parser.dom = parser.html_engine.parse_dom(source)
        return parser

    def take(self, **fields):
        parser = self.clone()
        for field, taker in fields.items():
            parser.state.data[field] = self._taker(taker).take(self.dom)
        return parser

    def exists(self, xpath):
        return bool(len(self.dom.xpath(xpath)))

    def foreach(self, xpath):
        for item in self.dom.xpath(xpath):
            if isinstance(item, str):
                yield item
            else:
                parser = self.clone()
                parser.dom = item
                yield parser

    def get(self, taker):
        return self._taker(taker).take(self.dom)

    def get_list(self, taker):
        return self._taker(taker).take_list(self.dom)

    def _taker(self, taker):
        if isinstance(taker, str):
            return XPathTaker(taker)
        return taker

    # def json(self, url):
    #     response = requests.get(url)
    #     return response.json()

    @property
    def source(self):
        return str(self.dom)

    @property
    def document(self):
        return self.state.data


class Config(object):

    def __init__(self):
        self.rss = RSSConfig()
        self.html = HTMLConfig()




