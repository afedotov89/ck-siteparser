# -*- coding: utf-8 -*-
from unittest import TestCase

import requests

from siteparser.parser import Parser


class TestRSS(TestCase):

    def test_telega_in(self):
        parser = Parser()
        parser = parser.html('https://telega.in/orders/new')
        # import ipdb; ipdb.set_trace()
        for subj_parser in parser.foreach('//select[@id="channel_theme"]/option'):
            subj_parser = subj_parser.take(subject='.')
            subject_id = subj_parser.get('./@value')
            if not subject_id:
                continue
            page = 1
            print('subj_id={}'.format(subject_id))
            while True:
                print(page)
                channels_json = requests.get(
                    'https://telega.in/orders/new.json?theme={}&page={}'.format(subject_id, page)
                ).json()
                channels_html = channels_json['html']
                print(channels_html)
                channels_parser = subj_parser.html(channels_html)
                for channel_parser in channels_parser.foreach('//tr'):
                    channel_parser = channel_parser.take(
                        url='./td[1]/a/@href',
                        cost='.//span[@class="cost"]'
                    )
                    print(channel_parser.document)
                if channels_json['show_more_btn']:
                    page += 1
                else:
                    break

            # subj_parser = item.html('https://telega.in/orders/new?theme={}'.format(subject_id))

            pass

        pass
