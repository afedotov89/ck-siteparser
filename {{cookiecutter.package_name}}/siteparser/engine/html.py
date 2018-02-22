# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import requests
from lxml import html, etree


class HTMLEngine(object):

    def __init__(self, config, request_headers=None):
        self.config = config
        self.request_headers = request_headers or {}

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
            return etree.tostring(self.root, pretty_print=True)

    def load_dom(self, url):
        r = requests.get(url, headers=self.request_headers)
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

    def __init__(self, request_headers=None):
        self.request_headers = request_headers or {}


class XPathTaker(object):

    def __init__(self, xpath):
        self.xpath = xpath

    def take(self, dom):
        return dom.xpath_text(self.xpath)