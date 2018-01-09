# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['bcy.net']
    start_urls = ['https://bcy.net/coser/toppost100',
			'https://bcy.net/coser/toppost100?type=week&date=20180106',
			'https://bcy.net/coser/toppost100?type=week&date=20180105']

    def parse(self, response):
        for a in response.css('a.cut.db.fz16.text'):
            yield { a.css('a::text').extract_first() : a.css('a::attr(href)').extract_first()}
