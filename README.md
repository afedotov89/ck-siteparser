siteparser
==============================

A convenient library for everyday parsing of sites

Install
-------

    # TODO

Usage
-----

    >>> from siteparser.parser import Parser
    >>> parser = Parser().html('https://www.kinopoisk.ru/top/')
    >>> docs = [
            sub_parser.take(
                title='./td[2]/a',
                original_title='./td[2]/span',
                vote='./td[3]//a'
            ).document
            for sub_parser in parser.foreach('//tr[contains(@id, "top250_place_")]')
        ]
    >>> len(docs)
    250
    >>> docs[0]
    {'title': 'Побег из Шоушенка (1994)', 'original_title': 'The Shawshank Redemption', 'vote': '9.191'}

