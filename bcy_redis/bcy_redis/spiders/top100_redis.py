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
    '''
    yield scrapy.FormRequest(
            url = 'https://bcy.net/coser/index/ajaxloadtoppost',
            formdata = {"p" : "1", "type" : "week"},
            callback = self.parse
        )
    '''
    def parse(self, response):
        request_date = str(response.url)[-8:]
        
        for i in range(1,4):
            yield scrapy.FormRequest(
                url = 'https://bcy.net/coser/index/ajaxloadtoppost?date='+request_date,
                formdata = {"p" : str(i), "type" : u"week", "date":request_date},
                callback = self.form_parse,dont_filter=True)
        
        for a in response.css('li._box'):
            item = BcyRedisItem()
            item['rank'] = a.css('span::text').extract_first()
            item['title'] = a.css('a::attr(title)').extract_first()
            item['date'] = response.url[-8:]
            if a.css('a::attr(href)').extract_first():
                item['url'] = 'https://bcy.net'+a.css('a::attr(href)').extract()[2]
                item['link'] = a.css('a::attr(href)').extract_first()
                next_page = 'https://bcy.net' + a.css('a::attr(href)').extract_first()
                if next_page is not None:
                    yield scrapy.Request(next_page, meta={'key':item},callback=self.ablum_parse,dont_filter=True)
            else:
                item['state']=''
                item['city']=''
                item['url']=''
                item['link'] = ''
                item['auth_url']=''
                item['auth_name']=''
                item['cartoon_name'] = ''
                item['following'] = ''
                item['follower'] = ''
                yield item

    def form_parse(self, response):
        for a in response.css('li._box'):
            item = BcyRedisItem()
            item['rank'] = a.css('span::text').extract_first()
            item['title'] = a.css('a::attr(title)').extract_first()
            item['date'] = response.url[-8:]
            if a.css('a::attr(href)').extract_first():
                item['url'] = 'https://bcy.net'+a.css('a::attr(href)').extract()[2]
                item['link'] = a.css('a::attr(href)').extract_first()
                next_page = 'https://bcy.net' + a.css('a::attr(href)').extract_first()
                if next_page is not None:
                    yield scrapy.Request(next_page, meta={'key':item},callback=self.ablum_parse,dont_filter=True)
            else:
                item['state']=''
                item['city']=''
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
        item['auth_name'] = response.css('a.fz14.dib.maxw250.cut::text').extract_first()
        if response.css('a._tag._tag--normal.cut.db::text') :
            item['cartoon_name'] = response.css('a._tag._tag--normal.cut.db::text').extract()[1].strip()
            item['following'] = response.css('a.vhr__item.minor::text').extract_first()[10:].strip()
            item['follower'] = response.css('a.tal.vhr__item.vhr__item--last.minor::text').extract_first()[10:].strip()
        else:
            item['cartoon_name'] = ''
            item['following'] = ''
            item['follower'] = ''
        yield scrapy.Request(item['url'], meta={'key':item},callback=self.auth_parse,dont_filter=True)

    def auth_parse(self,response):
        item = response.meta['key']
        b = response.xpath('//script[@id="tpl-profile-body"]')
        locate = re.findall(r'<p class="text fz14 lh1d4 mb15">(.+?)</p>',str(b.extract_first()))[1].decode() 
        #print locate
        #re.findall(r'<p class="text fz14 lh1d4 mb15">(.+?)</p>',str(b.extract()).decode())[1] 
        #locate = response.css('span.fz14::text').extract_first()
        locate_list = []
        locate_list = locate.split()
        item['state']=locate_list[0]
        item['city']=''
        if len(locate_list) >=2:
            item['city']=locate_list[1]
        
        print '>>>>>>>>>>==========RANK========='
        print item['rank']
        print '>>>>>>>>>>==========END========='
        yield item


