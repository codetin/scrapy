# -*- coding: utf-8 -*-
#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import datetime
from bcy.items import BcyItem

class ExampleSpider(scrapy.Spider):
    #fileobj = open('out.txt','w+')
    name = 'top100'
    allowed_domains = ['bcy.net']
    now = datetime.datetime.now()
    start_urls = []
    for i in range(0,1):
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=i)
        n_days = now - delta
        #print n_days.strftime('%Y%m%d')
        start_urls.append('https://bcy.net/coser/toppost100?type=week&date='+n_days.strftime('%Y%m%d'))
        #print repr(start_urls)
    def parse(self, response):
        for a in response.css('li.l-work-thumbnail'):
            item = BcyItem()
            item['rank'] = a.css('span::text').extract_first()
            item['url'] = response.url
            item['title'] = a.css('a::attr(title)').extract_first()
            if a.css('a::attr(href)').extract_first():
                item['link'] = a.css('a::attr(href)').extract_first()
                next_page = 'https://bcy.net' + a.css('a::attr(href)').extract_first()
                if next_page is not None:
                    #print "next_page_link:" + next_page
                    yield scrapy.Request(next_page, meta={'key':item},callback=self.auth_parse,dont_filter=True)
                #yield item
            else:
                item['link'] = ''
                item['auth_url']=''
                item['auth_name']=''
                item['cartoon_name'] = ''
                item['following'] = ''
                item['follower'] = ''
                yield item

                

    def auth_parse(self,response):
        item = response.meta['key']
        item['auth_url'] = response.url

        #print 'auth_url' + response.url

        item['auth_name'] = response.css('a.fz14.blue1::text').extract_first()
        if response.css('div.btn__text-wrap::text') :
            item['cartoon_name'] = trim(response.css('div.btn__text-wrap::text')[3].extract())
            item['following'] = trim(response.css('a.vhr__item.minor::text').extract_first()[10:])
            item['follower'] = trim(response.css('a.tal.vhr__item.vhr__item--last.minor::text').extract_first()[10:])
        else:
            item['cartoon_name'] = ''
            item['following'] = ''
            item['follower'] = ''
        yield item
