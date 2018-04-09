# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import requests
from lxml import html, etree


class HTMLEngine(object):

    def __init__(self, config):
        self.config = config

    class DOM(object):

        def __init__(self, root):
            self.root = root

        def xpath(self, xpath):
            return [
                item if isinstance(item, str) else self.__class__(item)
                for item in self.root.xpath(xpath)
            ]

        def xpath_text(self, xpath):
            item = self.root.xpath(xpath)
            if len(item):
                item = item[0]
            else:
                return ''
            text = self._dom_item_to_text(item)
            return text

        def xpath_text_list(self, xpath):
            items = self.root.xpath(xpath)
            text_list = [
                self._dom_item_to_text(item)
                for item in items
            ]
            return text_list

        def _dom_item_to_text(self, item):
            if isinstance(item, str):
                text = item
            else:
                text = item.text_content()
            text = text.replace(
                '\xa0', ' '  # Заменяем &nbsp;
            ).replace(
                '\r', '\n'
            )
            text = re.sub('[\u00b6]', '', text)
            text = re.sub(r'[\s\n]+\n', '\n', text)
            text = re.sub(r'[ \t]+', ' ', text)
            text = text.strip()
            return text

        def __str__(self):
            # FIXME hardcode encoding
            return etree.tostring(self.root, pretty_print=True).decode('utf8')

    def load_dom(self, url):
        r = requests.get(url, headers=self.config.request_headers, proxies=self.config.proxies)
        parser_kwargs = {}
        if 'charset' in r.headers.get('content-type') and r.encoding:
            parser_kwargs['encoding'] = r.encoding
        parser = html.HTMLParser(**parser_kwargs)
        tree = html.document_fromstring(r.content, parser=parser, base_url=url)
        return self.DOM(tree)

    def parse_dom(self, content, encoding=None, base_url=None):
        parser_kwargs = {}
        if encoding:
            parser_kwargs['encoding'] = encoding
        parser = html.HTMLParser(**parser_kwargs)
        tree = html.document_fromstring(content, parser=parser, base_url=base_url)
        return self.DOM(tree)


class HTMLConfig(object):

    def __init__(self, request_headers=None, proxies=None):
        self.request_headers = request_headers or {}
        self.proxies = proxies or {}


class XPathTaker(object):

    def __init__(self, xpath, strip=True):
        self.xpath = xpath
        self.strip = strip

    def take(self, dom):
        text = dom.xpath_text(self.xpath)
        if self.strip:
            text = text.strip()
        return text

    def take_list(self, dom):
        return dom.xpath_text_list(self.xpath)
