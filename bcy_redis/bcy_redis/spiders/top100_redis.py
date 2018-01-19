# -*- coding: utf-8 -*-
#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import datetime
#from scrapy.linkextractors import LinkExtractor
#from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisSpider
from bcy_redis.items import BcyRedisItem 
import re

class RedisSpider(RedisSpider):
    #fileobj = open('out.txt','w+')
    name = 'top100_redis'
    allowed_domains = ['bcy.net']
    redis_key = 'RedisSpider:start_urls'
    now = datetime.datetime.now()
    def parse(self, response):
        for a in response.css('li.l-work-thumbnail'):
            item = BcyRedisItem()
            item['rank'] = a.css('span::text').extract_first()
            item['title'] = a.css('a::attr(title)').extract_first()
            item['date'] = response.url[-8:]
            if a.css('a::attr(href)').extract_first():
                item['url'] = 'https://bcy.net'+a.css('a::attr(href)').extract()[3]
                item['link'] = a.css('a::attr(href)').extract_first()
                next_page = 'https://bcy.net' + a.css('a::attr(href)').extract_first()
                if next_page is not None:
                    yield scrapy.Request(next_page, meta={'key':item},callback=self.ablum_parse,dont_filter=True)
            else:
                item['location']=''
                item['url']=''
                item['link'] = ''
                item['auth_url']=''
                item['auth_name']=''
                item['cartoon_name'] = ''
                item['following'] = ''
                item['follower'] = ''
                yield item



    def ablum_parse(self,response):
        item = response.meta['key']
        item['auth_url'] = response.url
        print item['auth_url']
        item['auth_name'] = response.css('a.fz14.blue1::text').extract_first()
        if response.css('div.btn__text-wrap::text') :
            item['cartoon_name'] = response.css('div.btn__text-wrap::text')[3].extract().strip()
            item['following'] = response.css('a.vhr__item.minor::text').extract_first()[10:].strip()
            item['follower'] = response.css('a.tal.vhr__item.vhr__item--last.minor::text').extract_first()[10:].strip()
        else:
            item['cartoon_name'] = ''
            item['following'] = ''
            item['follower'] = ''
        yield scrapy.Request(item['url'], meta={'key':item},callback=self.auth_parse,dont_filter=True)

    def auth_parse(self,response):
        item = response.meta['key']
        item['location'] = response.css('span.fz14::text').extract_first()
        yield item


