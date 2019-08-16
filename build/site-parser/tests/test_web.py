# -*- coding: utf-8 -*-
from unittest import TestCase

import requests

from siteparser.parser import Parser


class TestRSS(TestCase):

    def test_telega_in(self):
        parser = Parser()
        parser = parser.html('https://telega.in/orders/new')
        # # import ipdb; ipdb.set_trace()
        # for subj_parser in parser.foreach('//select[@id="channel_theme"]/option'):
        #     subj_parser = subj_parser.take(subject='.')
        #     subject_id = subj_parser.get('./@value')
        #     if not subject_id:
        #         continue
        #     page = 1
        #     print('subj_id={}'.format(subject_id))
        #     while True:
        #         print(page)
        #         channels_json = requests.get(
        #             'https://telega.in/orders/new.json?theme={}&page={}'.format(subject_id, page)
        #         ).json()
        #         channels_html = channels_json['html']
        #         print(channels_html)
        #         channels_parser = subj_parser.html(channels_html)
        #         for channel_parser in channels_parser.foreach('//tr'):
        #             channel_parser = channel_parser.take(
        #                 url='./td[1]/a/@href',
        #                 cost='.//span[@class="cost"]'
        #             )
        #             print(channel_parser.document)
        #         if channels_json['show_more_btn']:
        #             page += 1
        #         else:
        #             break

    def test_tg_channel(self):
        parser = Parser()
        parser = parser.html('https://t.me/crypto_world_nevs')
        parser = parser.take(
            title='//div[@class="tgme_page_title"]',
            members_text='//div[@class="tgme_page_extra"]',
            description='//div[@class="tgme_page_description"]',
            photo='//img[@class="tgme_page_photo_image"]/@src'
        )
        print(parser.document)

    def test_get(self):
        parser = Parser()
        parser = parser.html('https://t.me/tvkinoradio/416?embed=1')
        self.assertEquals(
            parser.get('//div[@class="tgme_widget_message_link"]'),
            't.me/tvkinoradio/416'
        )
        self.assertSequenceEqual(
            parser.get_list('//div[@class="tgme_widget_message_text"]//a/@href'),
            ['https://t.me/jump_cut', 'https://t.me/jump_cut']
        )

    def test_exists(self):
        parser = Parser()
        parser = parser.html('https://t.me/elonmusknewsru/1?embed=1')
        self.assertFalse(parser.exists('//div[@class="tgme_widget_message_error" and text()="Post not found"]'))
        parser = parser.html('https://t.me/elonmusknewsru/100500?embed=1')
        self.assertTrue(parser.exists('//div[@class="tgme_widget_message_error" and text()="Post not found"]'))


